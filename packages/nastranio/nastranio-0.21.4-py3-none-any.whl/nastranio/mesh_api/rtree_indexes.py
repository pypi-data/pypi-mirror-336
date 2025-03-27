import logging
from functools import wraps

import numpy as np
from rtree import index

RTREE_COORDS_DEC = 2


def check_coords(*argnames):
    def _check_coords(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for argname in argnames:
                kwargs[argname] = list(
                    np.round(kwargs[argname], decimals=RTREE_COORDS_DEC)
                )
            return fn(*args, **kwargs)

        return wrapper

    return _check_coords


def list_content(rtree):
    for item in list(rtree.intersection(rtree.bounds, objects=True)):
        print(item)


class RTrees:
    """
    https://rtree.readthedocs.io/en/latest/tutorial.html
    """

    def __init__(self, registry, index_elems=("0d", "1d", "2d", "3d")):
        p = index.Property()
        p.dimension = 3
        self._rtree_properties = p
        # p.dat_extension = 'data'
        # p.idx_extension = 'index'
        self._ixs = {"GRID": index.Index(properties=self._rtree_properties)}
        self.index_elems = index_elems
        self.reg = registry

    def list(self, cardname=None, rtree=None):
        if rtree is None:
            rtree = self._ixs[cardname]
        return tuple(rtree.intersection(rtree.bounds, objects=True))

    def create_rtree(self, eids=None, gids=None):
        """create and return 'on-the-fly' a new rtree"""
        if eids is not None and gids is not None:
            raise ValueError("both `eids` and `gids` cannot be set")
        _rtree = index.Index(properties=self._rtree_properties)
        ids = eids if eids is not None else gids
        if gids is not None:
            src_rtrees = (self._ixs["GRID"],)
        else:
            src_rtrees = []
            for cardname, rtree in self._ixs.items():
                if cardname == "GRID":
                    continue
                src_rtrees.append(rtree)
        for rtree in src_rtrees:
            for item in list(rtree.intersection(rtree.bounds, objects=True)):
                if item.id in ids:
                    _rtree.insert(item.id, item.bbox)
        return _rtree

    # check_coords("coords")
    def add_grid(self, gid, /, coords, rtree=None):
        """insert gid in RTREE index"""
        self._ixs["GRID"].insert(int(gid), coords)
        if rtree:
            rtree.insert(int(gid), coords)

    # check_coords("coords")
    def add_elem(self, cardname, eid, /, coords, rtree=None):
        try:
            # if a pandas.Series is passed
            coords = coords.values
        except AttributeError:
            pass
        self._ixs[cardname].insert(int(eid), coords)
        if rtree:
            rtree.insert(int(eid), coords)

    # check_coords("old_coords", "coords")
    def _update(self, cardname, id, /, old_coords, coords, rtree=None):
        rt = self._ixs.get(cardname)
        if rt is None and rtree is None:
            return
        rt.delete(id, old_coords)
        rt.insert(id, coords)
        if rtree:
            rtree.delete(id, old_coords)
            rtree.insert(id, coords)

    def get_bbox(self, cardname, id):
        ix = self._ixs[cardname]
        for f in ix.intersection(ix.bounds, objects=True):
            if f.id == id:
                return f.bbox

    def get_gid_bbox(self, gid):
        return self.get_bbox(cardname="GRID", id=gid)
        ix = self._ixs["GRID"]
        for f in ix.intersection(ix.bounds, objects=True):
            if f.id == id:
                return f.bbox

    def get_eid_bbox(self, eid, cardname=None):
        if cardname:
            return self.get_bbox(cardname=cardname, id=eid)
        for cardname, ix in self._ixs.items():
            if cardname == "GRID":
                continue
            bbox = self.get_bbox(cardname=cardname, id=eid)
            if bbox is not None:
                return bbox

    def update_grid(self, gid, /, old_coords, coords, rtree=None):
        return self._update(
            "GRID", gid, old_coords=old_coords, coords=coords, rtree=rtree
        )

    def update_element(self, eid, /, old_coords, coords, rtree=None):
        # old_coords is taken from
        try:
            cardname = self.reg.mesh.eid2card(skipcache=True)[eid]
        except:
            # breakpoint()
            raise
        return self._update(
            cardname, eid, old_coords=old_coords, coords=coords, rtree=rtree
        )

    def build(self):
        # add all grids to objects
        grids = self.reg.container["bulk"]["GRID"].array[["ID", "X1", "X2", "X3"]]
        grids = np.lib.recfunctions.structured_to_unstructured(grids)
        for row in grids:
            self.add_grid(row[0], coords=row[1:])
        # ===============================================
        # add elements
        eid2bbox = self.reg.mesh.eid2bbox()
        cards = self.reg.container["summary"]["element"]
        for dim in self.index_elems:
            cards = self.reg.container["summary"][dim]
            for cardname in cards:
                card = self.reg.container["bulk"][cardname]
                self._ixs[cardname] = index.Index(properties=self._rtree_properties)
                for i, (eid, gids) in enumerate(card.eid2gids().items()):
                    bbox = eid2bbox.loc[eid]
                    self.add_elem(cardname, eid, coords=bbox)

    def nearest_grids(self, /, coords, num_results=1, astype=set, rtree=None):
        if not rtree:
            rtree = self._ixs["GRID"]
        return astype(rtree.nearest(coords, num_results))

    def nearest_elements(
        self, coords, num_results=1, astype=set, cardname=None, rtree=None
    ):
        if rtree:
            return astype(rtree.nearest(coords, num_results))
        if cardname:
            ix = self._ixs[cardname]
            return astype(ix.nearest(coords, num_results))
        # get all ids
        ids = {}
        for cardname, ix in self._ixs.items():
            if cardname == "GRID":
                continue
            ids[cardname] = astype(ix.nearest(coords, num_results))
        return ids
