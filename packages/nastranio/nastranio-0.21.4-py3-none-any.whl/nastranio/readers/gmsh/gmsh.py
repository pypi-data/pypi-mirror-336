import logging
from collections import defaultdict, namedtuple
from functools import cached_property
from pathlib import Path

import numpy as np

from nastranio.readers.gmsh.mixins import Modificator

Entity = namedtuple("Entity", ["entityDim", "entityTag", "bbox", "physical_tags"])
PhysicalGroup = namedtuple("PhysicalGroup", ["dim", "physical_tag", "name"])
Node = namedtuple("Node", ["gid", "entity", "x", "y", "z"])
Element = namedtuple(
    "Element",
    [
        "eid",
        "gids",
        "entity_dim",
        "entity_tag",
        "element_type",
        "physical_tags",
        "physical_groups",
    ],
)


def revert_dict(d):
    newd = defaultdict(set)
    # if `d` is kind of {k: (iterable)}
    if isinstance(next(iter(d.values())), (tuple, list, set)):
        for k, v in d.items():
            for subv in v:
                newd[subv].add(k)
    else:
        for k, v in d.items():
            newd[v] = k
    return dict(newd)


class GmsHParser(Modificator):
    def __init__(self, filepath):
        self.read(filepath)

    def info(self):
        msg = ""
        msg += f"Mesh Format {self._mesh_format}\n"
        msg += f"nb. nodes: {len(self.nodes)}\n"
        msg += f"nb. elements: {len(self.elements)}\n"
        cnt_types = {k: len(v) for k, v in self.type2eid.items()}
        for typ, nb in cnt_types.items():
            msg += f"   Type {typ}: {nb} elements\n"
        coincident_gids = self.coincident_nodes()
        if coincident_gids:
            msg += f"Coincident gids: {coincident_gids}\n"
        return msg

    def coincident_nodes(self, digits=0):
        xyzs = np.array([[n.gid, n.x, n.y, n.z] for gid, n in self.nodes.items()])
        gids = xyzs[:, 0].astype(int)
        xyzs = xyzs[:, 1:]
        if digits:
            xyzs = np.round(xyzs, digits)
        dedup_values, count = np.unique(xyzs, axis=0, return_counts=True)
        ix2gid = dict(zip(range(len(gids)), gids))
        repeated_groups = dedup_values[count > 1]
        coincident_gids = []
        for repeated_group in repeated_groups:
            repeated_idx = np.argwhere(np.all(xyzs == repeated_group, axis=1)).ravel()
            repeated_idx = (ix2gid[ix] for ix in repeated_idx)
            coincident_gids.append(tuple(repeated_idx))
        return coincident_gids

    def read(self, filepath):
        with open(filepath) as fh:
            self._toc = {}
            self._build_toc(fh.readlines())
        for section in self._toc.keys():
            process_func = f"_process_{section}"
            if hasattr(self, process_func):
                getattr(self, process_func)()
            else:
                logging.warning(f"no processing function for {section}")
        self._make_gid_eid_type()
        self._make_eid_gid_physicalGroups()

    # =========================================================================
    # a few helpers
    # =========================================================================
    # @cached_property
    # def type2eid(self):
    #     eid2type = defaultdict(set)
    #     for eid, elt in self.elements.items():
    #         eid2type[elt.element_type].add(eid)
    #     return dict(eid2type)

    @cached_property
    def dim2eid(self):
        eid2type = defaultdict(set)
        for eid, elt in self.elements.items():
            eid2type[elt.entity_dim].add(eid)
        return dict(eid2type)

    @cached_property
    def dim2physical_group(self):
        dim2pg = defaultdict(set)
        for (dim, _id), pg in self.physical_groups.items():
            dim2pg[pg.dim].add(pg)
        return dict(dim2pg)

    def _make_gid_eid_type(self):
        """build:

        * self.eid2gids
        * self.gid2eids
        * self.type2eid
        * self.eid2type

        """
        eid2gids = {}
        gid2eids = defaultdict(set)
        type2eid = defaultdict(set)
        eid2type = {}
        for eid, elt in self.elements.items():
            eid2gids[eid] = set(elt.gids)
            type2eid[elt.element_type].add(eid)
            eid2type[eid] = elt.element_type
            for gid in elt.gids:
                gid2eids[gid].add(eid)
        self.eid2gids = eid2gids
        self.type2eid = dict(type2eid)
        self.gid2eids = dict(gid2eids)
        self.eid2type = eid2type

    def _make_eid_gid_physicalGroups(self):
        """build:

        * self.eid2physical_groups
        * self.physical_group2eids
        * self.physical_group2gids
        * self.gid2physical_groups

        """
        self.eid2physical_groups = {
            eid: set(elt.physical_groups) for eid, elt in self.elements.items()
        }
        physical_group2eids = defaultdict(set)
        gid2physical_groups = defaultdict(set)
        physical_group2gids = defaultdict(set)
        for eid, grps in self.eid2physical_groups.items():
            gids = self.eid2gids[eid]
            for grp in grps:
                physical_group2eids[grp].add(eid)
                physical_group2gids[grp] |= gids
            for gid in gids:
                gid2physical_groups[gid] |= grps
        self.physical_group2eids = dict(physical_group2eids)
        self.physical_group2gids = dict(physical_group2gids)
        self.gid2physical_groups = dict(gid2physical_groups)

    # =========================================================================
    # internal stuff
    # =========================================================================

    def _build_toc(self, content):
        buffer = []
        IN_SECTION = None
        for line in content:
            line = line.split("//")[0].strip()
            if line.startswith("//"):
                continue
            if line.startswith("$End"):
                assert line[4:] == IN_SECTION
                self._toc[IN_SECTION] = buffer[:]
                buffer = []
                continue
            if line.startswith("$"):
                IN_SECTION = line[1:]
                continue
            buffer.append(line)

    def _process_MeshFormat(self):
        """creates self.mesh_format"""
        self._mesh_format = self._toc["MeshFormat"][0].split()[0]

    def _process_PhysicalNames(self):
        """
        creates `self.physical_groups` mapping (dim, physical tag) to physicalGroup named tuple
        """
        content = self._toc["PhysicalNames"]
        nb_physical_names = int(content.pop(0))
        data = {}
        for line in content:
            dim, physical_tag, *name = line.split()
            dim = int(dim)
            name = " ".join(name)
            _ = PhysicalGroup(dim, int(physical_tag), name.strip('"'))
            data[(dim, _.physical_tag)] = _
        self.physical_groups = data

    def _process_Entities_1d2d3d(self, nb, content, dim):
        for _ in range(nb):
            itemdata = content.pop(0)
            if dim == 0:
                entityTag, minX, minY, minZ, *groups = itemdata.split()
                bbox = (minX, minY, minZ)
            else:
                (
                    entityTag,
                    minX,
                    minY,
                    minZ,
                    maxX,
                    maxY,
                    maxZ,
                    *groups,
                ) = itemdata.split()
                bbox = (minX, minY, minZ, maxX, maxY, maxZ)
            entityTag = int(entityTag)
            # processing numPhysicalTags
            numPhysicalTags = int(groups.pop(0))
            physicalTags = groups[:numPhysicalTags]
            assert numPhysicalTags == len(physicalTags)
            groups = groups[numPhysicalTags:]
            if dim == 0:
                assert len(groups) == 0
            else:
                # should be finished here with 0d
                numBounding = int(groups[0])
                pointTags = list(map(int, groups[1:]))
                assert len(pointTags) == numBounding
            entity = Entity(
                entityDim=dim,
                entityTag=entityTag,
                bbox=tuple(map(float, bbox)),
                physical_tags=tuple(map(int, physicalTags)),
            )
            self.entities[dim][entityTag] = entity
        return content

    def _process_Entities(self):
        """
        creates a `self.entities` dictionnary, mapping
        {0: {entityTag: {"bbox": (0, 0, 0), "physicalTags": []}}}
        """
        content = self._toc["Entities"]
        self.entities = {k: defaultdict(dict) for k in range(4)}
        nb = content.pop(0).split()
        # ----------------------------------------------------------------
        # processing points
        numPoints, numCurves, numSurfaces, numVolumes = map(int, nb)
        content = self._process_Entities_1d2d3d(numPoints, content, 0)
        content = self._process_Entities_1d2d3d(numCurves, content, 1)
        content = self._process_Entities_1d2d3d(numSurfaces, content, 2)
        content = self._process_Entities_1d2d3d(numVolumes, content, 3)
        self.entities = {dim: dict(data) for dim, data in self.entities.items()}

    def _process_Nodes(self):
        content = self._toc["Nodes"]
        numEntityBlocks, numNodes, minNodeTag, maxNodeTag = map(
            int, content.pop(0).split()
        )
        self.nodes = {}

        for blockno in range(numEntityBlocks):
            entityDim, entityTag, parametric, numNodesInBlock = map(
                int, content.pop(0).split()
            )
            if numNodesInBlock == 0:
                continue
            node_ids = tuple(map(int, ",".join(content[:numNodesInBlock]).split(",")))
            xyzs = "\n".join(content[numNodesInBlock : numNodesInBlock * 2])
            content = content[2 * numNodesInBlock :]
            xyzs = np.fromstring(xyzs, dtype=float, sep=" ")
            xyzs = xyzs.reshape(int(len(xyzs) / 3), 3)
            for i, gid in enumerate(node_ids):
                xyz = xyzs[i]
                node = Node(
                    gid=gid,
                    entity=self.entities[entityDim][entityTag],
                    x=xyz[0],
                    y=xyz[1],
                    z=xyz[2],
                )
                self.nodes[gid] = node

    def _process_Elements(self):
        self.elements = {}
        # ---------------------------------------------------------------------
        # parse content
        content = self._toc["Elements"]
        numEntityBlocks, numElements, minElementTag, maxElementTag = map(
            int, content.pop(0).split()
        )

        for blockno in range(numEntityBlocks):
            entityDim, entityTag, elementType, numElementsInBlock = map(
                int, content.pop(0).split()
            )
            physicalTags = tuple(self.entities[entityDim][entityTag].physical_tags)
            try:
                physicalNames = tuple(
                    (
                        self.physical_groups[(entityDim, id_)].name
                        for id_ in physicalTags
                    )
                )
            except KeyError:
                # GMSH V4.12 API changes???
                physicalNames = tuple(
                    (
                        self.physical_groups[(entityDim, -id_)].name
                        for id_ in physicalTags
                    )
                )
            buffer = content[:numElementsInBlock]
            content = content[numElementsInBlock:]
            for row in buffer:
                eid_and_gids = map(int, row.split())
                eid, *gids = eid_and_gids
                element = Element(
                    eid=eid,
                    gids=tuple(gids),
                    entity_dim=entityDim,
                    entity_tag=entityTag,
                    element_type=elementType,
                    physical_tags=physicalTags,
                    physical_groups=physicalNames,
                )
                self.elements[eid] = element

    if __name__ == "__main__":
        import doctest

        doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
