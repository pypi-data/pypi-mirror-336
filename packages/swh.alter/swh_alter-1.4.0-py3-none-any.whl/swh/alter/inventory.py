# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""
This module implements the inventory stage of the
:ref:`removal algorithm <alter_removal_algorithm>`.
"""

from contextlib import suppress
import itertools
import logging
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

from igraph import Vertex

from swh.core.api.classes import stream_results, stream_results_optional
from swh.graph.http_client import GraphArgumentException, RemoteGraphClient
from swh.model.model import Origin, Revision
from swh.model.swhids import ExtendedObjectType as ObjectType
from swh.model.swhids import ExtendedSWHID
from swh.storage.algos.origin import iter_origin_visit_statuses, iter_origin_visits
from swh.storage.algos.snapshot import snapshot_get_all_branches
from swh.storage.interface import StorageInterface

from .progressbar import ProgressBar, ProgressBarInit, no_progressbar
from .subgraph import Subgraph
from .utils import filter_objects_missing_from_storage

logger = logging.getLogger(__name__)


class RootsNotFound(Exception):
    def __init__(self, swhids: Iterable[ExtendedSWHID]):
        self.swhids = list(sorted(swhids))

    def get_labels(self, requested: Collection[Origin | ExtendedSWHID]) -> List[str]:
        """Returns a list of either an origin URL if it can be found in requested and the
        SWHID otherwise."""

        return [
            next(
                (
                    x.url
                    for x in requested
                    if isinstance(x, Origin) and x.swhid() == swhid
                ),
                str(swhid),
            )
            for swhid in self.swhids
        ]


class StuckInventoryException(Exception):
    def __init__(self, swhids: List[ExtendedSWHID]):
        self.swhids = swhids


ITERATIONS_BEFORE_FORFEIT = 6


class InventorySubgraph(Subgraph):
    """A subgraph holding an inventory of all candidates for removal

    When all references from a given node have been accounted for,
    the ``complete`` attribute is set to True.
    """

    default_vertex_attributes: Dict[str, Any] = {"complete": False}

    def __init__(self, *args, **kwargs):
        """See :py:class:`Subgraph`"""
        super().__init__(*args, **kwargs)
        self["name"] = "Inventory"
        self["root_swhids"] = []
        if "complete" not in self.vs.attributes():
            self.vs["complete"] = [False for _ in self.vs]

    def select_incomplete(self) -> List[Vertex]:
        """Return vertices known to be incomplete ordered by object type from
        origins to contents."""

        # We want to order incomplete vertices from origin to content in order to
        # increase the chance to complete as many vertices as possible using swh.graph
        # traversal which follows the same direction.
        return self.select_ordered(complete_eq=False)

    def dot_node_attributes(self, v: Vertex) -> List[str]:
        """Get a list of attributes in DOT format for the given vertex.

        On top of default attributes, use a bold font for root objects, and color the background
        if the vertex is known to be incomplete.

        :meta private:
        """
        attrs = super().dot_node_attributes(v)
        if v["swhid"] in self["root_swhids"]:
            attrs.append('fontname="times bold"')
        if not v["complete"]:
            attrs.append("color=gray")
        return attrs


class Lister:
    """A class encapsulating our inventory algorithm.

    :meta private:
    """

    def __init__(
        self,
        storage: StorageInterface,
        graph_client: RemoteGraphClient,
        subgraph: InventorySubgraph,
        /,
        known_missing: Optional[Set[ExtendedSWHID]] = None,
        progressbar: Optional[ProgressBar] = None,
    ):
        self._subgraph = subgraph
        self._storage = storage
        self._graph_client = graph_client
        self._known_missing = known_missing or set()
        self._progressbar = progressbar

    @property
    def subgraph(self):
        return self._subgraph

    def inventory_candidates(self, root: ExtendedSWHID) -> None:
        self._subgraph["root_swhids"].append(root)
        # Add our starting point as incomplete
        self._subgraph.add_swhid(root, complete=False)
        # Iterate until everything has been fetched
        logger.debug("inventory_candidates: added %s", root)
        stats_history: List[Tuple[int, int]] = []
        for remaining in self._iter_inventory_candidates():
            total = len(self._subgraph.vs)
            stats_history.append((total, remaining))
            # Does the last iterations always have the same stats?
            if (
                len(stats_history) > ITERATIONS_BEFORE_FORFEIT
                and len(set(stats_history[-ITERATIONS_BEFORE_FORFEIT:])) == 1
            ):
                raise StuckInventoryException(
                    [vertex["swhid"] for vertex in self._subgraph.select_incomplete()]
                )
            if self._progressbar:
                self._progressbar.update(
                    1, current_item=ProgressBarItem(root, total, remaining)
                )
            logger.debug(
                "inventory_candidates: %4d SWHIDS known, %4d need to be looked up.",
                total,
                remaining,
            )
        if self._progressbar:
            self._progressbar.update(
                1, current_item=ProgressBarItem(None, len(self._subgraph.vs), 0)
            )

    def _fetch_candidates_using_graph(self, vertex) -> None:
        # We don’t except all SWHID to be present in swh.graph
        with suppress(GraphArgumentException):
            self.add_edges_traversing_graph(vertex["swhid"])

    def _fetch_candidates_using_storage(self, vertex) -> None:
        self.add_edges_using_storage(vertex["swhid"])

    def _iter_inventory_candidates(self) -> Iterator[int]:
        # We cycle from retrieving from swh.graph (fast but potentially incomplete),
        # and swh.storage (complete, but slow and one level at a time).
        # Note: SWHIDs discovered from swh.graph will not
        # require further fetching. Because objects are immutable,
        # nothing could have been added after the graph has been
        # exported. The sole exception is origin objects.
        # References from SWHIDs discovered from swh.storage
        # have to be looked up though. As there is a chance they
        # can be found them in swh.graph, we’ll do that at our
        # next iteration.
        fetchers = itertools.cycle(
            [self._fetch_candidates_using_graph, self._fetch_candidates_using_storage]
        )
        while to_fetch := [
            v
            for v in self._subgraph.select_incomplete()
            if v["swhid"] not in self._known_missing
        ]:
            yield len(to_fetch)
            fetch = next(fetchers)
            for vertex in to_fetch:
                # fetcher might complete more than a given vertex, so
                # this one might just have been completed since we got
                # the list of incomplete vertices
                if vertex["complete"]:
                    continue
                fetch(vertex)

    def add_edges_traversing_graph(self, start: ExtendedSWHID) -> None:
        # Mapping between SWHID string and integer vertex index
        swhid_vertices: Dict[str, int] = {}

        # SWHIDs that haven't been added yet, and whether they will be complete
        pending_swhids: Set[str] = set()

        # All SWHID -> SWHID edges seen so far
        seen_edges: Set[Tuple[str, str]] = set()

        # Edges that still need to be added
        pending_edges: Set[Tuple[str, str]] = set()

        def add_swhid(swhid):
            """Record a swhid to be added to the subgraph"""
            if swhid in swhid_vertices:
                return

            pending_swhids.add(swhid)

        def add_edge(src, dst):
            """Record an edge to be added to the subgraph"""
            edge = (src, dst)
            if edge in seen_edges:
                return

            add_swhid(src)
            add_swhid(dst)
            pending_edges.add((src, dst))
            seen_edges.add((src, dst))

            # Add new edges in bulk
            if len(pending_edges) > 10000:
                flush_edges()

        def flush_edges():
            """Add all the pending swhids, and all pending edges, to the subgraph."""

            # Check for swhids that are already in the subgraph and record them
            # in swhid_vertices
            found = {
                v["name"]: v.index
                for v in self._subgraph.vs.select(name_in=pending_swhids)
            }
            swhid_vertices.update(found)

            # Filter the really new swhids and insert them
            new_swhids = pending_swhids - found.keys()
            if new_swhids:
                added = self._subgraph.add_swhids(new_swhids)
                swhid_vertices.update(added)

            # Mark all non-origin nodes as completely visited
            for name in pending_swhids:
                if not name.startswith("swh:1:ori:"):
                    self._subgraph.vs[swhid_vertices[name]]["complete"] = True

            pending_swhids.clear()

            # Then, add the edges in bulk
            self._subgraph.add_edges(
                (swhid_vertices[src], swhid_vertices[dst]) for src, dst in pending_edges
            )
            pending_edges.clear()

        # We want everything except dir→rev edges which represent submodules.
        # See the relevant comment in `_add_edges_using_storage_for_directory` below.
        edge_restriction = "ori:*,snp:*,rel:*,rev:*,dir:dir,dir:cnt"

        # XXX: We should be able to pass a SWHID object to visit_edges()
        for src, dst in self._graph_client.visit_edges(
            str(start), edges=edge_restriction
        ):
            add_edge(src, dst)

        # Always manually flush the last batch of swhids/edges
        flush_edges()

    def add_edges_using_storage(self, source: ExtendedSWHID) -> None:
        _ADD_EDGES_USING_STORAGE_METHODS_PER_OBJECT_TYPE[source.object_type](
            self, source
        )

    def _add_edges_using_storage_for_content(self, source: ExtendedSWHID) -> None:
        _ = self._subgraph.add_swhid(source, complete=True)
        # Nothing is referenced by content objects so we have no edges to add

    def _add_edges_using_storage_for_directory(self, source: ExtendedSWHID) -> None:
        v_directory = self._subgraph.add_swhid(source, complete=True)
        entries = stream_results_optional(
            self._storage.directory_get_entries, source.object_id
        )
        if not entries:
            logger.warning("Directory %s not found", source)
            return
        for entry in entries:
            target = entry.swhid().to_extended()

            # References from directory to revision represents submodules. As of
            # April 2023, loaders will record the reference to a submodule, and
            # that’s it. They don’t handle loading the associated origin. If the
            # revision for a submodule is in the archive, it means that we the
            # origin has been retrieved separately. The policy is thus that to
            # remove the code in a submodule, one should remove the associated
            # origin. Long story short, revisions used as submodule (and their
            # references) are not considered as candidates for removal when
            # inventorying a directory.
            if target.object_type == ObjectType.REVISION:
                logger.debug(
                    "Ignored submodule %s (%s), listed in directory %s",
                    entry.name,
                    entry.swhid(),
                    source,
                )
                continue

            # Content objects are our leafs. Therefore we already know all about
            # them as soon as we know they exist and we can consider them complete.
            if target.object_type == ObjectType.CONTENT:
                v_target = self._subgraph.add_swhid(target, complete=True)
            else:
                v_target = self._subgraph.add_swhid(target)
            # It is possible to get the same target multiple times
            # for a single directory. For example if it contains multiple
            # files with the same content.
            self._subgraph.add_edge(v_directory, v_target, skip_duplicates=True)

    def _add_edges_using_storage_for_revision(self, source: ExtendedSWHID) -> None:
        # We limit the search to not retrieve too much at once from storage.
        # We will have to retrieve the oldest parent revisions if needed in any cases.
        for rev_d in self._storage.revision_log([source.object_id], limit=100):
            if rev_d is None:
                continue
            elif isinstance(rev_d, Revision):
                revision = rev_d
            else:
                # TODO: remove this conditional once swh-storage fully migrated to
                # returning revision objects instead of dicts
                revision = Revision.from_dict(rev_d)
            revision_swhid = revision.swhid().to_extended()
            # We might know about this revision already from a previous revision
            # log, we can skip it. We can't skip further commits though, as the
            # history doesn't have to be strictly linear.
            if self._subgraph.vs.select(name=str(revision_swhid), complete=True):
                continue
            # We can say these don’t need to be fetched as we know that
            # we are getting everything about this revision here:
            # its directory and parents.
            v_revision = self._subgraph.add_swhid(revision_swhid, complete=True)
            v_directory = self._subgraph.add_swhid(revision.directory_swhid())
            self._subgraph.add_edge(v_revision, v_directory)
            # We create a set here because some revisions point to the same
            # parent multiple times.
            for parent_swhid in set(revision.parent_swhids()):
                v_parent = self._subgraph.add_swhid(parent_swhid)
                self._subgraph.add_edge(v_revision, v_parent)

    def _add_edges_using_storage_for_release(self, source: ExtendedSWHID) -> None:
        v_release = self._subgraph.add_swhid(source, complete=True)
        [release] = self._storage.release_get([source.object_id])
        if not release:
            logger.warning("Release %s not found", source)
            return
        v_target = self._subgraph.add_swhid(release.target_swhid())
        self._subgraph.add_edge(v_release, v_target)

    def _add_edges_using_storage_for_snapshot(self, source: ExtendedSWHID) -> None:
        v_snapshot = self._subgraph.add_swhid(source, complete=True)
        snapshot = snapshot_get_all_branches(self._storage, source.object_id)
        if not snapshot:
            logger.warning("Snapshot %s not found", source)
            return
        # We need to deduplicate targets as multiple branches can point to the
        # same head and we only need one edge for each target.
        # TODO: Better document aliases in swh-model. I had to look at mercurial
        #       loader to understand what they were useful for.
        # We also skip aliases here as they are referring to a branch name
        # inside the snapshot. As we inventory the reference for every branches
        # the branch pointed by an alias will always be dealt with.
        target_swhids = {
            branch.swhid()
            for branch in snapshot.branches.values()
            if branch and branch.target_type.value != "alias"
        }
        for swhid in target_swhids:
            v_branch = self._subgraph.add_swhid(swhid)
            self._subgraph.add_edge(v_snapshot, v_branch)

    def _add_edges_using_storage_for_origin(self, source: ExtendedSWHID) -> None:
        v_source = self._subgraph.add_swhid(source, complete=True)
        [origin_d] = self._storage.origin_get_by_sha1([source.object_id])
        if not origin_d:
            raise ValueError(f"Origin “{source}” not found in storage")
        for visit in iter_origin_visits(self._storage, origin_d["url"]):
            assert visit.visit is not None  # make mypy happy
            for status in iter_origin_visit_statuses(
                self._storage, visit.origin, visit.visit
            ):
                snapshot_swhid = status.snapshot_swhid()
                if snapshot_swhid:
                    v_snapshot = self._subgraph.add_swhid(snapshot_swhid)
                    self._subgraph.add_edge(v_source, v_snapshot, skip_duplicates=True)


_ADD_EDGES_USING_STORAGE_METHODS_PER_OBJECT_TYPE: Dict[
    ObjectType, Callable[[Lister, ExtendedSWHID], None]
] = {
    ObjectType.CONTENT: Lister._add_edges_using_storage_for_content,
    ObjectType.DIRECTORY: Lister._add_edges_using_storage_for_directory,
    ObjectType.REVISION: Lister._add_edges_using_storage_for_revision,
    ObjectType.RELEASE: Lister._add_edges_using_storage_for_release,
    ObjectType.SNAPSHOT: Lister._add_edges_using_storage_for_snapshot,
    ObjectType.ORIGIN: Lister._add_edges_using_storage_for_origin,
}


class ProgressBarItem(NamedTuple):
    origin: Optional[ExtendedSWHID]
    total: int
    remaining: int

    def __str__(self) -> str:
        return (
            f"{self.origin or 'done'} "
            f"({self.total} objects found / {self.remaining} left to look up)"
        )


def _ensure_swhids_exist_in_storage(
    storage: StorageInterface, swhids: List[ExtendedSWHID]
) -> None:
    """Raise RootsNotFound if any of the given swhids cannot be found
    in the given storage."""

    wanted_swhids = set(swhids)
    existing_swhids = set(filter_objects_missing_from_storage(storage, wanted_swhids))
    diff = wanted_swhids - existing_swhids
    if diff:
        raise RootsNotFound(diff)


def make_inventory(
    storage,
    graph_client,
    swhids: List[ExtendedSWHID],
    known_missing: Optional[Set[ExtendedSWHID]] = None,
    progressbar: Optional[ProgressBarInit] = None,
) -> InventorySubgraph:
    """Inventory candidates for removal from the given set of SWHID.

    By querying the given `storage` and `graph_client`, create a subgraph
    with all objects belonging to the given set of SWHIDs (typically origins).
    The result should then used to verify which candidate can safely be
    removed.
    """

    _ensure_swhids_exist_in_storage(storage, swhids)

    subgraph = InventorySubgraph()
    known_missing = known_missing or set()
    progressbar_init: ProgressBarInit = progressbar or no_progressbar
    bar: ProgressBar[ProgressBarItem]
    with progressbar_init(
        # Giving an infinite iterator is one of the rare ways
        # to get click.progressbar() to display a moving cursor.
        # In any cases, we are not going to use its value as we
        # manually call `.update()` in `Lister.inventory_candidates()`.
        # But we still need to make mypy happy and give the right
        # type for the progressbar item.
        itertools.cycle([ProgressBarItem(swhids[0], 0, 0)]),
        label="Inventorying all reachable objects…",
        show_percent=False,
        show_pos=False,
        item_show_func=lambda s: str(s) if s else "",
    ) as bar:
        lister = Lister(
            storage,
            graph_client,
            subgraph,
            known_missing=known_missing,
            progressbar=bar,
        )
        for swhid in swhids:
            lister.inventory_candidates(swhid)
    return lister.subgraph


def get_raw_extrinsic_metadata(
    storage: StorageInterface,
    referencing_swhids: List[ExtendedSWHID],
    progressbar: Optional[ProgressBarInit] = None,
) -> Iterator[ExtendedSWHID]:
    """Find RawExtrinsicMetadata referencing the given SWHIDs.

    This will recursively find RawExtrinsicMetadata referencing
    the found RawExtrinsicMetadata objects. The output is sorted
    in the order of the iterations: the objects coming first are
    referenced by objects latter in the list.
    """
    progressbar_init: ProgressBarInit = progressbar or no_progressbar
    more_label = ""
    while len(referencing_swhids) > 0:
        found_swhids = []
        with progressbar_init(
            referencing_swhids,
            label=f"Finding {more_label}RawExtrinsicMetadata objects…",
        ) as bar:
            for target_swhid in bar:
                authorities = storage.raw_extrinsic_metadata_get_authorities(
                    target_swhid
                )
                for authority in authorities:
                    for emd in stream_results(
                        storage.raw_extrinsic_metadata_get, target_swhid, authority
                    ):
                        found_swhids.append(emd.swhid())
        yield from found_swhids
        referencing_swhids = found_swhids
        more_label = f"more {more_label}"
