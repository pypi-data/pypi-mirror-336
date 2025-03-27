"""
Mesh API
"""

import logging
import os
import warnings
from collections import Counter, defaultdict
from io import BytesIO
from itertools import chain, combinations

import numpy as np
import pandas as pd

try:
    import pyvista as pv

    ISPYVISTA = True
except ImportError:
    ISPYVISTA = False
import vg

try:
    import vtk

    ISVTK = True
except ImportError:
    ISVTK = False

from numtools.csyslib import Register as CSysReg
from numtools.intzip import hzip
from numtools.vgextended import angle as angle_0_pi
from numtools.vgextended import loc_array

import nastranio.cards as cards_mod
from nastranio.constants import BULK, ELEMENT, PROPERTY, shapes
from nastranio.decorators import cached_property, profile, timeit
from nastranio.utils import array2dic, bunch, dic2array

try:
    import networkx as nx

    HAS_NX = True
except ImportError:
    HAS_NX = False

GMSH_STR_SEP = "#"


def dedup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class Mesh:
    """
    API to operate on a Registry records
    """

    def _list_caches(self):
        return {k for k in self.__dict__ if k.startswith(cached_property.CACHED_PREFIX)}

    def clear_caches(self, rebuild=True):
        """delete internal caches"""
        prefix = cached_property.CACHED_PREFIX
        cache_names = self._list_caches()  # _cache_XXX
        cached_names = [k.replace(prefix, "") for k in cache_names]  # XXX
        logging.info("clean cached properties: %s", ", ".join(cached_names))
        for fcached, cache_name in zip(cached_names, cache_names):
            self.__dict__.pop(cache_name)
        # ---------------------------------------------------------------------
        # rebuilding
        _rebuilt = []
        if rebuild:
            for fcached, cache_name in zip(cached_names, cache_names):
                # fcached = cached_name.replace(prefix, "")
                getattr(self, fcached)
                _rebuilt.append(fcached)
        if _rebuilt:
            logging.info("rebuilt cache: %s", ", ".join(_rebuilt))

    def set_registry(self, registry, calc_csys=False):
        """Bind a registry to the Mesh instance"""
        self.reg = registry
        self.CSys = None
        # build coordinate systems
        if calc_csys:
            self.calc_csys()

    def calc_csys(self):
        self.CSys = CSysReg(minid=0)
        # create CSYS0
        self.CSys.new(
            id=0,
            origin=(0, 0, 0),
            axis=[(1, 0, 0), (0, 1, 0), (0, 0, 1)],
            title="Reference Rectangular Coordinate System",
            labels=("X1", "X2", "X3"),
        )
        if "CORD2R" not in self.reg.container["bulk"]:
            # no defined CSys
            return
        arr = self.reg.container["bulk"]["CORD2R"].array
        # --------------------------------------------------------------------
        # sort CSYS by reference IDs to create CSYS in the correct order
        df = pd.DataFrame(arr).set_index(["RID", "CID"]).sort_index()

        titles = self.reg.comments().get("Coordinate System", {})
        for (rid, cid), points in df.iterrows():
            self.CSys.new(
                id=cid,
                reference_id=rid,
                points=(
                    (points["A1"], points["A2"], points["A3"]),
                    (points["B1"], points["B2"], points["B3"]),
                    (points["C1"], points["C2"], points["C3"]),
                ),
                title=titles.get(cid, "Rectangular Coordinate System"),
                labels=("X1", "X2", "X3"),
            )

    def cquad4_axis(self, digits=5):
        # ====================================================================
        # ⚠ NOTE ⚠
        # --------------------------------------------------------------------
        # WORK IN PROGRESS
        # --------------------------------------------------------------------
        # nic@alcazar -- dimanche 1 décembre 2019, 09:00:07 (UTC+0100)
        # mercurial: fbd21002395c+ tip
        # ====================================================================
        grids = self.reg.container[BULK.title]["GRID"]
        grids_df = grids.coords(asdf=True)
        cardobj = self.reg.CQUAD4
        eids = cardobj.eid2gids(asdf=True).stack()
        eids.index.names = ["EID", "GID"]
        eids.name = "gid"
        eids = eids.to_frame()
        df = (
            pd.merge(eids, grids_df, right_index=True, left_on="gid")
            .sort_index()
            .unstack(level=-1)[["X", "Y", "Z"]]
            .swaplevel(axis=1)
            .T.sort_index()
            .T[cardobj.gids_header]
        )

        _G1G2 = df["G2"].values - df["G1"].values
        _G1G3 = df["G3"].values - df["G1"].values

        # --------------------------------------------------------------------
        # calculate Z (normal)
        Z = np.round(vg.normalize(vg.cross(_G1G2, _G1G3)), digits)
        df[[("Zelem", "X"), ("Zelem", "Y"), ("Zelem", "Z")]] = pd.DataFrame(
            Z, index=df.index
        )
        # --------------------------------------------------------------------
        # calculate X
        _G2G4 = df["G4"].values - df["G2"].values
        df[[("_G2G4", "X"), ("_G2G4", "Y"), ("_G2G4", "Z")]] = pd.DataFrame(
            _G2G4, index=df.index
        )

        β = vg.angle(_G1G2, _G1G3)
        γ = vg.angle(_G2G4, -_G1G2)
        α = (β + γ) / 2
        df["α"] = α
        gps = df.groupby([("α", ""), ("Zelem", "X"), ("Zelem", "Y"), ("Zelem", "Z")])
        # "_gpid" identify group of processing
        df["_gpid"] = gps.ngroup()
        Xs = {}
        for (angle, *axis), _df in gps:
            key = set(_df._gpid)
            assert len(key) == 1
            key = next(iter(key))
            Xs[key] = vg.normalize(
                vg.rotate(_df._G2G4.values, around_axis=np.array(axis), angle=angle)
            )
        # X = pd.DataFrame(
        #     vg.rotate(-df._G2G4.values, Z.values, df['α'].values), index=df.index
        # )
        # df[[('Xelem', 'X'), ('Xelem', 'Y'), ('Xelem', 'Z')]] = X
        return df, Xs

    # ========================================================================
    # coords
    # ========================================================================

    def coords(self, incsys=None, eids=None, gids=None, asdf=False):
        """
        Return coordinates of all or subset of grid points.

        :param incsys: Coordinate System to output coordinates
        :type incsys: None or  integer
        :param eids: Elements IDs providing a subset of grid points IDs
        :type eids: Iterable of integers
        :param gids: iterable of grid poit IDs to query coordinates
        :type gids: Iterable of integers
        :param asdf: "As DataFrame". If True, return a pandas DataFrame
        :type asdf: bool

        :returns: either a tuple (gids, coordinates, coordinates system IDs) or pandas DataFrame.

        if `eids` and `gids` are provided, `gids` will be ignored.

        Proxy method to `loading.GRIDS.coords()`

        >>> gids, coords, csys = reg.mesh.coords()
        >>> gids
        array([    1,     2, ..., 12516, 12517])
        >>> coords
        array([[374.79303586, -47.79179422,  14.66539227],
               [374.793     , -46.965     ,  14.6654 ],
               ...,
               [372.45      , -42.28      ,   0.     ],
               [363.95      , -42.28      ,   0.     ]])
        >>> csys
        array([0, 0, 0, ..., 0, 0, 0])


        Providing `gids` to get selected coordinates:

        >>> gids, coords, csys = reg.mesh.coords(gids=((1,12517)))
        >>> gids
        array([    1,  12517])
        >>> coords
        array([[374.79303586, -47.79179422,  14.66539227],
               [363.95      , -42.28      ,   0.     ]])
        >>> csys
        array([0, 0])


        Providing `eids` to automatically select grid points, and requesting
        a pandas dataframe:

        >>> reg.mesh.coords(eids=((1,)), asdf=True)
             csys        X        Y        Z
        gid
        5       0  375.856 -47.4020  14.6654
        12      0  375.686 -47.6245  14.6654
        13      0  375.331 -47.3115  14.6654
        15      0  375.216 -47.5571  14.6654

        """
        gridcards = self.reg.container[BULK.title]["GRID"]
        if eids:
            gids = self.eid2gids(eids=eids, asbunch=True)
        if incsys is not None:
            if self.CSys is None:
                self.calc_csys()
            csysreg = self.CSys
        else:
            csysreg = None
        coords = gridcards.coords(incsys=incsys, csysreg=csysreg, gids=gids, asdf=asdf)
        return coords

    # ========================================================================
    # normals
    # ========================================================================

    def normals(self, eids=None, strict=False, digits=3, silent_warnings=True):
        """return normalized normals for 1D and 2D elements as pandas dataframe.
        Elements IDs can optionally be provided to select a subset of elements.

        :param eids: IDs to calculate normals
        :type eids: iterable of integers
        :param strict: Wether or not raise an exception if an invalid element ID is
            provided
        :type strict: bool
        :param digits: number of digits to keep after rounding
        :type digits: int

        :returns: pandas DataFrame

        In the following examples, element #203 doesn't exist. By default, invalid
        elements are silently skipped.

        >>> reg.mesh.normals(eids=(1, 2, 203))
             X    Y    Z
        1  0.0  0.0 -1.0
        2 -0.0  0.0 -1.0
        >>> # Using `strict=True` will raise an exception:
        >>> reg.mesh.normals(eids=(1, 2, 203), strict=True)
        Traceback (most recent call last):
            ...
        ValueError: elements IDs {203} doesn`t exist or doesn`t have a normal.

        For 1D elements, the `normal` is set to be the GA-GB vector. This makes handy
        to calculate the angle between a 1D element and a 2D element.

        In the following example, CBUSHes #11137 and 11138 have coincidents points.

        >>> cbushes_id = reg.mesh.eids_by_cards(('CBUSH',))
        >>> cbushes_id
        {11137, 11138, ..., 11175, 11176}
        >>> reg.mesh.normals(cbushes_id)
                 X    Y    Z
        11137  NaN  NaN  NaN
        11138  NaN  NaN  NaN
        ...
        11175  0.0  0.0 -1.0
        11176  0.0  0.0 -1.0

        """
        if silent_warnings:
            warnings.simplefilter("ignore")
        nn = self._elems_normal.copy()
        nn["data"] = np.round(nn["data"], digits)
        df = pd.DataFrame(**nn)
        if eids:
            # check if provided eids are OK (are they referring to 2D elems?)
            eids = set(eids)
            allowed = set(df.index)
            wrong_eids = eids - allowed
            if wrong_eids:
                msg = (
                    "elements IDs %s doesn`t exist or doesn`t have a normal."
                    % wrong_eids
                )

                if strict:
                    raise ValueError(msg)
                else:
                    logging.warning(msg)
            eids = eids & allowed
            df = df.loc[list(eids)]

        return df

    def geom_1d_elements(self, eids=None, cardnames=None):
        """
        >>> reg.mesh.geom_1d_elements().round(1)
                 GA     GB     XA    YA    ZA     XB    YB    ZB  GAGBx  GAGBy  GAGBz
        eid
        11137  7799  12516  372.4 -42.3   0.0  372.4 -42.3   0.0    0.0    0.0    0.0
        11138  7800  12517  364.0 -42.3   0.0  364.0 -42.3   0.0    0.0    0.0    0.0
        ...
        """
        coords = self.coords(incsys=0, asdf=True)[["X", "Y", "Z"]].copy()
        # select lineic elements
        arrays = []
        elems_cards = self.reg.summary["line"]  # 1D without RBE
        if not cardnames:
            cardobjs = self.reg.container[BULK.title]
        else:
            cardobjs = {
                cardname: cardobj
                for cardname, cardobj in self.reg.container[BULK.title].items()
                if cardname in cardnames
            }
        for cardname, cardobj in cardobjs.items():
            if cardname not in elems_cards:
                continue
            arrays.append(cardobj.array[[cardobj.XID_FIELDNAME] + cardobj.gids_header])

        array = np.hstack(arrays)
        df = pd.DataFrame(array).set_index("EID")  # drop cardname information
        df = df.merge(coords, left_on="GA", right_index=True).merge(
            coords, left_on="GB", right_index=True, suffixes=("A", "B")
        )
        df["GAGBx"] = df["XB"] - df["XA"]
        df["GAGBy"] = df["YB"] - df["YA"]
        df["GAGBz"] = df["ZB"] - df["ZA"]
        df.index.names = ["eid"]
        if eids:
            df = df.loc[eids]
        return df

    @cached_property
    def _geom_1d_elements_legacy(self):
        """return 4-items tuple:
        eids np.Array (n,), gagb np.Array(n, 3), GA coords (n, 3), GB Coords (n,3)
        """

        gids, coords, csys = self.coords(incsys=0)
        eids1d = []
        gids1d = []
        # select lineic elements
        elems_cards = self.reg.summary["line"]  # 1D without RBE
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            # eids1d = cardobj.eid2gids1d(asdf=True).stack()
            _eids1d = cardobj.eid2gids(keep_order=True)
            breakpoint()
            eids1d.append(list(_eids1d.keys()))
            gids1d.append(list(_eids1d.values()))
        # --------------------------------------------------------------------
        # keep the three first nodes only (enough to calculate normals)
        for i, _gids1d in enumerate(gids1d):
            _gids1d = np.array(_gids1d)
            gids1d[i] = _gids1d
        if eids1d:
            eids1d = np.concatenate(eids1d)
            # [eid1, eid2, ...] -> [eid1, eid1, eid1, eid2, eid2, eid2, ...]
            gids1d = np.concatenate(gids1d)
            # [[G1, G2, G3], [G1, G2, G3],...] -> [G11, G12, G13, G21, G22, G23, ...]

            # coordinates of nodes G1, G2 and G3 for eids1d elements
            GA = coords[loc_array(gids, gids1d[:, 0])]
            GB = coords[loc_array(gids, gids1d[:, 1])]

            ret = {"index": eids1d, "data": np.hstack((GA, GB, GB - GA))}
        else:
            ret = {
                "index": [],
                "data": [],
            }
        ret["columns"] = [
            "GAx",
            "GAy",
            "GAz",
            "GBx",
            "GBy",
            "GBz",
            "GAGBx",
            "GAGBy",
            "GAGBz",
        ]

        df = pd.DataFrame(**ret)
        df.index.names = ["eid"]
        return df

    @cached_property
    def _elems_normal(self):
        """calculate and return 2D elements normals"""
        gids, coords, csys = self.coords(incsys=0)
        dfs = []
        # ====================================================================
        # 2D elements
        # ====================================================================
        eids2d = []
        gids2d = []
        # cquad4 / ctria3
        elems_cards = self.reg.summary["2d"]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            # eids2d = cardobj.eid2gids2d(asdf=True).stack()
            _eids2d = cardobj.eid2gids(keep_order=True)
            eids2d.append(list(_eids2d.keys()))
            gids2d.append(list(_eids2d.values()))
        # --------------------------------------------------------------------
        # keep the three first nodes only (enough to calculate normals)
        for i, _gids2d in enumerate(gids2d):
            _gids2d = np.array(_gids2d)[:, :3]
            gids2d[i] = _gids2d
        if eids2d:
            eids2d = np.concatenate(eids2d)
            # [eid1, eid2, ...] -> [eid1, eid1, eid1, eid2, eid2, eid2, ...]
            gids2d = np.concatenate(gids2d)
            # [[G1, G2, G3], [G1, G2, G3],...] -> [G11, G12, G13, G21, G22, G23, ...]

            # coordinates of nodes G1, G2 and G3 for eids2d elements
            G1s = coords[loc_array(gids, gids2d[:, 0])]
            G2s = coords[loc_array(gids, gids2d[:, 1])]
            G3s = coords[loc_array(gids, gids2d[:, 2])]

            Z2d = vg.normalize(vg.cross((G2s - G1s), (G3s - G1s)))

        else:
            eids2d, Z2d = None, None
        # ====================================================================
        # 1D elements
        # ====================================================================
        eids1d = []
        gids1d = []
        # select lineic elements
        elems_cards = self.reg.summary.get("line", ())  # 1D without RBE
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            # eids1d = cardobj.eid2gids1d(asdf=True).stack()
            _eids1d = cardobj.eid2gids(keep_order=True)
            eids1d.append(list(_eids1d.keys()))
            gids1d.append(list(_eids1d.values()))
        # --------------------------------------------------------------------
        # keep the three first nodes only (enough to calculate normals)
        for i, _gids1d in enumerate(gids1d):
            _gids1d = np.array(_gids1d)[:, :2]
            gids1d[i] = _gids1d
        if eids1d:
            eids1d = np.concatenate(eids1d)
            # [eid1, eid2, ...] -> [eid1, eid1, eid1, eid2, eid2, eid2, ...]
            gids1d = np.concatenate(gids1d)
            # [[G1, G2, G3], [G1, G2, G3],...] -> [G11, G12, G13, G21, G22, G23, ...]

            # coordinates of nodes G1, G2 and G3 for eids1d elements
            G1s = coords[loc_array(gids, gids1d[:, 0])]
            G2s = coords[loc_array(gids, gids1d[:, 1])]

            Z1d = vg.normalize(G2s - G1s)
        else:
            eids1d, Z1d = None, None
        # ====================================================================
        # merge 1D and 2D
        # ====================================================================
        if eids1d is not None and eids2d is not None:
            eids = np.hstack((eids1d, eids2d))
            Z = np.vstack((Z1d, Z2d))
        elif eids1d is not None:
            eids = eids1d
            Z = Z1d
        else:
            eids = eids2d
            Z = Z2d
        return {"index": eids, "data": Z, "columns": ["X", "Y", "Z"]}

    def get_cbars_y_vector(self):
        """return a dataframe like:
                X1   X2   X3
        eid
        3      1.0  0.0  0.0
        4      1.0  0.0  0.0
        6      1.0  0.0  0.0
        ...
        """
        CBARS = self.reg.container["bulk"]["CBAR"]
        df = pd.DataFrame(CBARS.array)

        dfGO = df.dropna(subset=["GO"])
        if len(dfGO) > 0:
            raise NotImplementedError(
                "cannot calculate Y vector for elements defined with GO"
            )
        df = df[["EID", "X1", "X2", "X3"]].set_index("EID")
        df.index.names = ["eid"]
        return df

    # ========================================================================
    # area
    # ========================================================================
    @cached_property
    def _area_tria(self):
        """return area for triangular elements as a dict
        ready to be transformed in pandas Series
        """
        # --------------------------------------------------------------------
        # Triangles area are easy: (G1G2 ^ G1G3) / 2
        eids = sorted(list(self.eids_by_shape(shapes.TRIA)))
        if not eids:
            return {"index": [], "data": [], "name": "area"}
        gids, coords, csys = self.coords(incsys=0, eids=eids, asdf=False)
        # _coords = self.coords(incsys=0, eids=eids, asdf=True)
        eid2gids = self.eid2gids(eids=eids, keep_order=True)
        _eids, _gids = (
            np.array(list(eid2gids.keys())),
            np.array(list(eid2gids.values())),
        )
        G1s = coords[loc_array(gids, _gids[:, 0])]
        G2s = coords[loc_array(gids, _gids[:, 1])]
        G3s = coords[loc_array(gids, _gids[:, 2])]

        areas = np.linalg.norm(vg.cross((G2s - G1s), (G3s - G1s)), axis=1) / 2
        return {"index": _eids, "data": areas, "name": "area"}
        # quads_cards = self.reg.summary.get(shapes.QUAD)

    @cached_property
    def _area_quad(self):
        """return area for triangular elements as a dict
        ready to be transformed in pandas Series
        """
        # --------------------------------------------------------------------
        # Triangles area are easy: (G1G2 ^ G1G3) / 2
        eids = sorted(list(self.eids_by_shape(shapes.QUAD)))
        if not eids:
            return {"index": [], "data": [], "name": "area"}
        gids, coords, csys = self.coords(incsys=0, eids=eids, asdf=False)
        # _coords = self.coords(incsys=0, eids=eids, asdf=True)
        eid2gids = self.eid2gids(eids=eids, keep_order=True)
        _eids, _gids = (
            np.array(list(eid2gids.keys())),
            np.array(list(eid2gids.values())),
        )
        G1s = coords[loc_array(gids, _gids[:, 0])]
        G2s = coords[loc_array(gids, _gids[:, 1])]
        G3s = coords[loc_array(gids, _gids[:, 2])]
        G4s = coords[loc_array(gids, _gids[:, 3])]

        a1 = np.linalg.norm(vg.cross((G2s - G1s), (G3s - G1s)), axis=1) / 2
        a2 = np.linalg.norm(vg.cross((G3s - G1s), (G4s - G1s)), axis=1) / 2
        return {"index": _eids, "data": a1 + a2, "name": "area"}
        # quads_cards = self.reg.summary.get(shapes.QUAD)

    def get_all_eids(self, cards=None):
        """return all elements IDs as a set"""
        eids = set()
        all_cards = self.reg.container["summary"]["element"].copy()
        if not cards:
            cards = set()
        searched_cards = all_cards - cards
        for cardname in searched_cards:
            card = self.reg.container["bulk"][cardname]
            eids |= set(card.carddata["main"]["EID"])
        return eids

    @cached_property
    def _area(self):
        tri = self._area_tria
        quad = self._area_quad
        # all others elements have a null area
        all_eids = set(self.eid2gids().keys())
        null_ix = np.array(
            sorted(list(all_eids - (set(tri["index"]) | set(quad["index"]))))
        )
        x = np.arange(len(null_ix), dtype="float64")
        null_values = np.full_like(x, np.nan)

        return {
            "index": np.hstack((tri["index"], quad["index"], null_ix)),
            "data": np.hstack((tri["data"], quad["data"], null_values)),
            "name": "area",
        }

    def area(self, eids=None):
        """
        return areas of optinally provided elements IDs
        """
        areas = self._area.copy()
        if eids:
            eids = np.array(list(eids))
            ix = loc_array(areas["index"], eids)
            index = areas["index"][ix]
            data = areas["data"][ix]
            areas.update({"index": index, "data": data})
        return areas

    # ========================================================================
    # lengths
    # ========================================================================
    @cached_property
    def _length(self):
        """calcualte lengths for 2D elements and single-leg RBE*"""
        eids1d = []
        gids1d = []
        # --------------------------------------------------------------------
        # first, line lements (therefore excluding RBE*)
        _processed = self.reg.summary[shapes.LINE]
        cardnames = self.reg.summary[shapes.LINE]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in cardnames:
                continue
            _eids1d = cardobj.eid2gids(keep_order=True)
            if not _eids1d:
                continue
            eids1d.append(list(_eids1d.keys()))
            gids1d.append(np.array(list(_eids1d.values())))
        # --------------------------------------------------------------------
        # mono-legs RBE*
        cardnames = self.reg.summary["1d"]
        cardnames = cardnames - _processed  # remove LINE elements
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in cardnames:
                continue
            _eids1d = {
                k: v
                for k, v in cardobj.eid2gids(keep_order=True).items()
                if len(v) == 2
            }  # mono-legs RBE*
            if not _eids1d:
                continue
            gids1d.append(np.array(list(_eids1d.values())))
            eids1d.append(list(_eids1d.keys()))
        gids1d = np.vstack(gids1d)
        eids1d = np.hstack(eids1d)
        # --------------------------------------------------------------------
        # get coordinates
        gids, coords, csys = self.coords(incsys=0)
        G1s = coords[loc_array(gids, gids1d[:, 0])]
        G2s = coords[loc_array(gids, gids1d[:, 1])]

        lengths = vg.magnitude(G2s - G1s)

        return {"index": eids1d, "data": lengths, "name": "length"}

    def length(self, eids=None):
        """
        Return lengths for provided elements. If no elements are provided
        (``eids=None``), return the lengths for any 1D elements.

        Mono-legs RBE* are included.

        :param eids: *optional* element IDs to investigate.
        :type eids: sequence of integers

        :returns: lengths data dictionnary ready to be transformed in pandas Series

        >>> reg.mesh.length(eids=(11137, 11138))
        {'index': array([11137, 11138]), 'data': array([0., 0.]), 'name': 'length'}
        """
        lengths = self._length.copy()
        if eids:
            eids = np.array(list(eids))
            ix = loc_array(lengths["index"], eids)
            index = lengths["index"][ix]
            data = lengths["data"][ix]
            lengths.update({"index": index, "data": data})
        return lengths

    # ========================================================================
    # thicknesses
    # ========================================================================
    @cached_property
    def _thk(self):
        """return a pandas Series {eid: thk}"""
        # --------------------------------------------------------------------
        # get thicknesses defined in the elements
        elems_cards = self.reg.summary["2d"]
        ix = []
        data = []
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            _data = cardobj.thk
            ix.append(_data["index"])
            data.append(_data["data"])
        if not data:
            data = {"data": [], "index": [], "name": "elem_thk"}
        else:
            # prepare a series to make merge easier
            data = {"data": np.hstack(data), "index": np.hstack(ix), "name": "elem_thk"}
        eid2thk = pd.Series(**data, dtype="float64")
        # --------------------------------------------------------------------
        # get thicknesses defined by properties
        pid2thk = pd.Series(self.pid2thk(), name="prop_thk", dtype="float64")
        eid2pid = pd.Series(self.eid2pid(), name="pid")
        thks = pd.merge(eid2pid, pid2thk, left_on="pid", right_index=True, how="left")
        thks = thks.merge(eid2thk, left_index=True, right_index=True, how="left")
        return thks[["prop_thk", "elem_thk"]].max(axis=1).sort_index()

    def thk(self, eids=None, asdict=True):
        """return a mapping {eid: thk}

        >>> reg.mesh.thk(eids=(24, 27, 4, 35, 36, 37, 33, -1))
        {24: 0.09, 27: 0.09, 4: 0.09, 35: 0.09, 36: 0.09, 37: 0.09, 33: 0.09, -1: nan}
        """
        _thk = self._thk.copy()
        if eids:
            _thk = _thk.reindex(list(eids))
        if asdict:
            _thk = _thk.to_dict()
        return _thk

    # ========================================================================
    # gid2XXX
    # ========================================================================

    @cached_property
    def _gid2eids(self):
        """
        first part of gid2eids. Split to cache intermediate results
        """
        _gid2eids = defaultdict(set)
        for eid, _gids in self.eid2gids().items():
            for gid in _gids:
                _gid2eids[gid].add(eid)

        return {gid: frozenset(eids) for gid, eids in _gid2eids.items()}

    def gid2eids(self, gids=None, asbunch=False):
        """
        return a dictionnary with all gids as keys, and associated eids set.

        :param gids: optional subset of grid point IDs to check.
        :type gids: iterable of integers.

        :returns: dictionnary

        >>> reg.mesh.gid2eids()
        {13: frozenset({8, 1, 6, 7}), 12: frozenset({1, 2, 4, 9}), ...}
        >>> # A set of grid points can optionally be provided:
        >>> reg.mesh.gid2eids(gids=(1, 17))
        {1: frozenset({8, 9, 12}), 17: frozenset({10, 14})}
        >>> reg.mesh.gid2eids(gids=(1, 17), asbunch=True)
        frozenset({8, 9, 10, 12, 14})
        """
        # --------------------------------------------------------------------
        # test
        # if asbunch:
        #     eids = self._meetic[['gid', 'eid1', 'eid2']].set_index('gid')
        #     if gids:
        #         eids = eids.loc[list(gids)]
        #     return frozenset(set(eids.eid1) | set(eids.eid2))
        # # end of test
        # --------------------------------------------------------------------
        _gid2eids = self._gid2eids.copy()
        if gids:
            _gid2eids = {gid: _gid2eids[gid] for gid in gids}
        if asbunch:
            return bunch(_gid2eids)
        return _gid2eids

    def next_unused_gid(self):
        """return next free (unused) node ID, not using caches"""
        all_gids = self.reg.container["bulk"]["GRID"].carddata["main"]["ID"]
        return max(all_gids) + 1

    def next_unused_eid(self):
        """return next free (unused) element ID, not using caches"""
        cards = self.reg.container["summary"]["element"]
        all_eids = set()
        for cardname in cards:
            card = self.reg.container["bulk"][cardname]
            all_eids |= set(card.carddata["main"]["EID"])
        return max(all_eids) + 1

    # ========================================================================
    # card2XXX
    # ========================================================================
    @cached_property
    def _card2eids(self):
        ret = defaultdict(set)
        # to make docstrings more reliable, sort keys
        cards = sorted(list(self.reg.summary["element"]))
        for cardname in cards:
            card = self.reg.bulk[cardname]
            ret[cardname] = set(card.carddata["main"][card.EID_FIELDNAME])
        return dict(ret)

    def card2eids(self, cards=None):
        """
        return a dict mapping cardname to eids

        >>> reg.mesh.card2eids()
        {'CBUSH': {11137, ...}, 'CQUAD4': {1, ...}, 'CTRIA3': {5121, ...}, ...}
        >>> reg.mesh.card2eids(cards=('CQUAD4', 'CTRIA3'))
        {'CQUAD4': {1, ...}, 'CTRIA3': {5121, ...}
        """
        card2eids = self._card2eids.copy()
        if not cards:
            return card2eids
        return {k: v for k, v in card2eids.items() if k in cards}

    # ========================================================================
    # eid2XXX
    # ========================================================================

    @cached_property
    def _eid2gids_ordered(self):
        """
        first part of eid2gids(keep_order=True).
        Split to cache intermediate results"""
        _eid2gids = {}
        elems_cards = self.reg.summary["element"]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            _eid2gids.update(cardobj.eid2gids(keep_order=True))  #
        return dict(_eid2gids)

    @cached_property
    def _eid2gids(self):
        """
        first part of eid2gids(keep_order=False, asbunch=False).
        Split to cache intermediate results"""
        _eid2gids = {}
        elems_cards = self.reg.summary["element"]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            _eid2gids.update(cardobj.eid2gids(keep_order=False))  #
        return dict(_eid2gids)

    @cached_property
    def _eid2gids_asbunch(self):
        """
        first part of eid2gids(keep_order=False, asbunch=True).
        Split to cache intermediate results"""
        _gids = {}
        elems_cards = self.reg.summary["element"]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in elems_cards:
                continue
            _gids |= cardobj.eid2gids(keep_order=False)
        return _gids

    def eid2data(self, eids=None):
        """return a pandas DataFrame with misc data, sorted by `eid`:

        >>> reg.mesh.eid2data()
                 card dim   pid  length      area   thk    volume  const
        eid
        1      CQUAD4  2d     1     NaN  0.127690  0.09  0.011492  False
        2      CQUAD4  2d     1     NaN  0.176163  0.09  0.015855  False
        3      CQUAD4  2d     1     NaN  0.248014  0.09  0.022321  False
        4      CQUAD4  2d     1     NaN  0.130147  0.09  0.011713  False
        5      CQUAD4  2d     1     NaN  0.330996  0.09  0.029790  False
        ...       ...  ..   ...     ...       ...   ...       ...    ...
        12845    RBE2  1d  None     0.0       NaN   NaN       NaN  False
        12846    RBE2  1d  None     0.0       NaN   NaN       NaN  False
        12847    RBE2  1d  None     0.0       NaN   NaN       NaN  False
        12986    RBE3  1d  None     NaN       NaN   NaN       NaN  False
        12987    RBE3  1d  None     NaN       NaN   NaN       NaN  False
        <BLANKLINE>
        [4246 rows x 8 columns]
        """
        eid2data = self._eid2data.copy()
        if eids:
            eid2data = eid2data.loc[list(eids)]
        return eid2data

    @cached_property
    def _eid2data(self):
        """return a pandas DataFrame with misc data, sorted by `eid`:

        >>> reg.mesh.eid2data
                 card dim   pid
        eid
        1      CQUAD4  2d     1
        2      CQUAD4  2d     1
        ...       ...  ..   ...
        12986    RBE3  1d  None
        12987    RBE3  1d  None
        <BLANKLINE>
        [4246 rows x 3 columns]

        """
        ret = []
        cards = self.reg.summary[ELEMENT]
        for cardname in cards:
            _ret = {}
            card = self.reg.bulk[cardname]
            _carddata = dict(
                eid=card.array[card.EID_FIELDNAME].tolist(),
                card=[cardname] * len(card),
                dim=[card.dim] * len(card),
                # gmsh_eltype=[card.gmsh_eltype] * len(card),
                # shape=[card.shape] * len(card)
            )
            # pids are not just a repetition
            if hasattr(card, "PID_FIELDNAME"):
                pid = card.array[card.PID_FIELDNAME].tolist()
            else:
                pid = [None] * len(card)
            _carddata["pid"] = pid
            _ret = pd.DataFrame(_carddata).set_index("eid")
            ret.append(_ret)
        df = pd.concat(ret).sort_index()
        # --------------------------------------------------------------------
        # area and lengths
        df["length"] = pd.Series(**self.length())
        df["area"] = pd.Series(**self.area())
        try:
            df["thk"] = pd.Series(self.thk())
        except:
            df["thk"] = 0.0
        df["volume"] = df.area * df.thk
        # --------------------------------------------------------------------
        # boundaries
        gid2eids = self.gid2eids(self.boundaries.index.tolist())
        const_eids = [eid for eid in chain.from_iterable(gid2eids.values())]
        df["const"] = False
        df.loc[const_eids, "const"] = True
        return df

    def eid2gids(
        self, eids=None, dim=None, cards=None, keep_order=False, asbunch=False
    ):
        """
        return a dictionnary with all eids as keys, and associated gids set
        """
        # --------------------------------------------------------------------
        # define which property to use
        if asbunch:
            if keep_order:
                raise ValueError("`keep_order` is incompatible with `asbunch`")
            else:
                _eid2gids = self._eid2gids  # conversion to set will occur later on
        else:
            if keep_order:
                _eid2gids = self._eid2gids_ordered.copy()
            else:
                _eid2gids = self._eid2gids.copy()
        # --------------------------------------------------------------------
        # pre-select elements IDs
        if dim:
            eids = self.eids_by_dim(dim)
        elif cards:
            eids = self.eids_by_cards(cards)
        # --------------------------------------------------------------------
        # trigger property
        if eids:
            _eid2gids = {eid: _eid2gids.get(eid) for eid in eids}
        if asbunch:
            return bunch(_eid2gids)
            # _gids = set()
            # for gids in _eid2gids.values():
            #     _gids |= gids
            # return _gids
        return _eid2gids

    def get_eid_cardname(self, eid):
        """non-cached cardname searcher"""
        for cardname in self.reg.summary[ELEMENT]:
            card = self.reg.bulk[cardname]
            eids = card.carddata["main"][card.EID_FIELDNAME]
            if eid in eids:
                return cardname

    @cached_property
    def _eid2card(self):
        ret = {}
        cards = sorted(list(self.reg.summary[ELEMENT]))
        for cardname in cards:
            card = self.reg.bulk[cardname]
            eids = card.carddata["main"][card.EID_FIELDNAME]
            ret.update(dict(zip(eids, [cardname] * len(eids))))
        return ret

    def eid2card(self, eids=None, cards=None, asbunch=False, skipcache=False):
        """
        return a mapping {eid: cardname}

        :param eids: element IDs to filter
        :type eids: iterable of integers
        :param cards: cards to filter
        :type cards: iterable of valid card names

        :returns: dictionnary mapping element IDs to cardname

        >>> reg.mesh.eid2card()
        {11137: 'CBUSH', ..., 3688: 'CTRIA3', ...}
        >>> reg.mesh.eid2card(eids=(11137, 11139, 3689))
        {11137: 'CBUSH', 11139: 'CBUSH', 3689: 'CQUAD4'}
        >>> s = reg.mesh.eid2card(eids=(11137, 11139, 3689), asbunch=True)
        >>> s == frozenset({'CBUSH', 'CQUAD4'})
        True
        >>> reg.mesh.eid2card(eids=(11137, 11139, 3689), cards=('CQUAD4', 'CTRIA3'))
        {3689: 'CQUAD4'}

        """
        if skipcache:
            _d = {}
            _cards = sorted(list(self.reg.summary[ELEMENT]))
            for _cardname in _cards:
                _card = self.reg.bulk[_cardname]
                _eids = _card.carddata["main"][_card.EID_FIELDNAME]
                _d.update(dict(zip(_eids, [_cardname] * len(_eids))))
        else:
            _d = self._eid2card.copy()
        if eids:
            _d = {eid: card for eid, card in _d.items() if eid in eids}
        if cards:
            _d = {eid: card for eid, card in _d.items() if card in cards}
        if asbunch:
            return frozenset(_d.values())
        return _d

    @cached_property
    def _eid2dim(self):
        ret = {}
        cards = sorted(list(self.reg.summary[ELEMENT]))
        for cardname in cards:
            card = self.reg.bulk[cardname]
            eids = card.carddata["main"][card.EID_FIELDNAME]
            ret.update(dict(zip(eids, [card.dim] * len(eids))))
        return ret

    def eid2dim(self, eids=None, dims=None, asbunch=False):
        """
        return a mapping {eid: dim}

        :param eids: element IDs to filter
        :type eids: iterable of integers
        :param dims: dimensions to filter. (eg. '1d', '2d', '0d', etc...)
        :type dims: iterable of valid dimentsions names

        :returns: dictionnary mapping element IDs to dimension

        >>> reg.mesh.eid2dim()
        {11137: '1d', ..., 3688: '2d', ...}
        >>> reg.mesh.eid2dim(eids=(11137, 11139, 3689))
        {11137: '1d', 11139: '1d', 3689: '2d'}
        >>> s = reg.mesh.eid2dim(eids=(11137, 11139, 3689), asbunch=True)
        >>> s == frozenset({'1d', '2d'})
        True
        >>> reg.mesh.eid2dim(eids=(11137, 11139, 3689), dims=('1d', '0d', '3d'))
        {11137: '1d', 11139: '1d'}
        """
        _d = self._eid2dim.copy()
        if eids:
            _d = {eid: dim for eid, dim in _d.items() if eid in eids}
        if dims:
            _d = {eid: dim for eid, dim in _d.items() if dim in dims}
        if asbunch:
            return frozenset(_d.values())
        return _d

    @cached_property
    def _eid2shape(self):
        ret = {}
        cards = sorted(list(self.reg.summary[ELEMENT]))
        for cardname in cards:
            card = self.reg.bulk[cardname]
            eids = card.carddata["main"][card.EID_FIELDNAME]
            ret.update(dict(zip(eids, [card.shape] * len(eids))))
        return ret

    def eid2shape(self, eids=None, shapes=None, asbunch=False):
        """
        return a mapping {eid: shape}

        :param eids: element IDs to filter
        :type eids: iterable of integers
        :param shapes: shapeensions to filter. (eg. '1d', '2d', '0d', etc...)
        :type shapes: iterable of valid shapeentsions names

        :returns: dictionnary mapping element IDs to shapeension

        >>> reg.mesh.eid2shape()
        {11137: 'line', ..., 3688: 'triangle', ...}
        >>> reg.mesh.eid2shape(eids=(11137, 11139, 3689))
        {11137: 'line', 11139: 'line', 3689: 'quad'}
        >>> reg.mesh.eid2shape(eids=(11137, 11139, 3689), shapes=('triangle', 'quad', '3d'))
        {3689: 'quad'}
        >>> s = reg.mesh.eid2shape(eids=(11137, 11139, 3689), asbunch=True)
        >>> s == frozenset({'line', 'quad'})
        True
        """
        _d = self._eid2shape.copy()
        if eids:
            _d = {eid: shape for eid, shape in _d.items() if eid in eids}
        if shapes:
            _d = {eid: shape for eid, shape in _d.items() if shape in shapes}
        if asbunch:
            return frozenset(_d.values())
        return _d

    @cached_property
    def _eid2pid(self):
        """
        return a mapping {eid: pid}
        """
        ret = {}
        cards = self.reg.summary[ELEMENT]
        for cardname in cards:
            card = self.reg.bulk[cardname]
            if not hasattr(card, "PID_FIELDNAME"):
                logging.info(f"{cardname} has not PID_FIELDNAME attr. Skip")
                continue
            eids = card.carddata["main"][card.EID_FIELDNAME]
            pids = card.carddata["main"][card.PID_FIELDNAME]
            ret.update(dict(zip(eids, pids)))
        return ret

    def eid2pid(self, eids=None, asbunch=False):
        """
        return a mapping {eid: pid}
        """
        eid2pid = self._eid2pid.copy()
        if eids:
            eid2pid = {eid: pid for eid, pid in eid2pid.items() if eid in eids}
        if asbunch:
            return frozenset(eid2pid.values())
        return eid2pid

    @cached_property
    def _pid2mids(self):
        pid2mids = {}
        for pname in self.reg.summary[PROPERTY]:
            prop = self.reg.bulk[pname]
            pid2mids.update(prop.pid2mids)
        return pid2mids

    def pid2mids(self, eids=None, pids=None, asbunch=False):
        """
        Return a dictionnary mapping PID to material IDs MIDS. If ``asbunch`` is
        ``True``, a single set of material IDs is returned.

        :param eids: *optional* restrict PIDs to element's property IDs
        :param pids: *optional* restrict PIDs to provided property IDs
        :param asbunch: should the mids be breakdowned by PID (``False``) or not
            (``True``)
        :type asbunch: bool

        :returns: ``dict`` or ``frozenset``

        >>> dic = reg.mesh.pid2mids()
        >>> dic == {1: frozenset({1}), 2: frozenset({1}), 4: frozenset({2, 3}),
        ...         5: frozenset({2, 4}), 6: frozenset({2, 4}), 7: frozenset({1, 5}),
        ...         8: frozenset(), 9: frozenset(), 10: frozenset()}
        True
        >>> reg.mesh.pid2mids(pids=(4,5), asbunch=True)
        frozenset({2, 3, 4})
        """
        pid2mids = self._pid2mids.copy()
        if eids:
            pids = self.eid2pid(eids=eids, asbunch=True)
        if pids:
            pid2mids = {pid: mids for pid, mids in pid2mids.items() if pid in pids}
        if asbunch:
            return bunch(pid2mids)
        return pid2mids

    @cached_property
    def _eid2mids(self):
        """
        return a mapping {eid: mid}
        """
        eid2pid = self._eid2pid.copy()
        return {eid: self._pid2mids[pid] for eid, pid in eid2pid.items()}

    def eid2mids(self, eids=None, asbunch=False):
        """
        Return a mapping {eid: mids}.

        :param eids: *optional* element IDs to investigate.
        :type eids: iterable of integer.

        :returns: ``dict`` (if ``asbunch`` is ``False``) or ``set`` (if ``asbunch`` is
            ``True``)

        >>> dic = reg.mesh.eid2mids(eids=(1, 5343))
        >>> dic == {5343: frozenset({2, 4}), 1: frozenset({1})}
        True
        """
        eid2mids = self._eid2mids.copy()
        if eids:
            eid2mids = {eid: mids for eid, mids in eid2mids.items() if eid in eids}
        if asbunch:
            return bunch(eid2mids)
        return eid2mids

    @cached_property
    def _eid2pcard(self):
        """
        return a mapping {EID: PCARD},
        eg. {1: 'PCOMP', 2: 'PBUSH', 3: 'PCOMP'}
        """
        ret = {}
        eid2pcard = {eid: self.pid2pcard()[pid] for eid, pid in self._eid2pid.items()}
        return eid2pcard

    def eid2pcard(self, eids=None, asbunch=False):
        """
        return a mapping {EID: PCARD},
        eg. {1: 'PCOMP', 2: 'PBUSH', 3: 'PCOMP'}
        """
        eid2pcard = self._eid2pcard.copy()
        if eids:
            eid2pcard = {eid: pcard for eid, pcard in eid2pcard.items() if eid in eids}
        if asbunch:
            return frozenset(eid2pcard.values())
        return eid2pcard

    # ========================================================================
    # eids_by_XXX
    # ========================================================================
    def eids_by_cards(self, cards=None):
        """
        return a unique set of eids defined by `cards` (any iterable).

        :param cards: cards defining elements to search
        :type cards: iterable of valid element card names

        :returns: a set of elements IDs

        >>> reg.mesh.eids_by_cards(cards=('CQUAD4', 'CBUSH'))
        {1, 2, 3, 4, ...}
        """
        if not cards:
            cards = self.reg.summary["element"]
        cards = set(cards)

        eids = set()
        for cardname in cards:
            card = self.reg.bulk[cardname]
            eids |= set(card.carddata["main"][card.EID_FIELDNAME])
        return eids

    def eids_by_dim(self, dim):
        """
        return a unique set of eids with provided dim. `dim` shall be one
        of {'0d', '1d', '2d', '3d'}.

        :param dim: dimension to search
        :type dim: string

        >>> reg.mesh.eids_by_dim(dim='0d')
         {11217, 11220}
        """
        assert dim in ("0d", "1d", "2d", "3d")
        cards = self.reg.summary.get(dim)
        if not cards:
            return set()
        return self.eids_by_cards(cards)

    def eids_by_shape(self, shape):
        """
        Return a unique set of eids with provided shape.

        >>> reg.mesh.eids_by_shape(shape='line')
        {11137, 11138, ..., 11175, 11176}

        ``shape`` shall be one of ``nastranio.constants.shapes``:

        >>> from nastranio.constants import shapes
        >>> shapes
        SHAPE(VERTICE='point', LINE='line', TRIA='triangle', QUAD='quad', MPC='mpc')
        >>> shapes.TRIA
        'triangle'
        """
        if shape not in shapes:
            raise ValueError(f"{shape} must be one of {shapes}")
        cards = self.reg.summary.get(shape)
        if not cards:
            return set()
        return self.eids_by_cards(cards)

    @cached_property
    def _pid2pcard(self):
        """
        return a dictionnary mapping Property ID <PID> to cardname <PCARD> {PID: PCARD}
        """
        pid2pcard = {}
        pcards = self.reg.summary[PROPERTY]
        for pcardname in pcards:
            pcard = self.reg.bulk[pcardname]
            pids = pcard.carddata["main"][pcard.PID_FIELDNAME]
            pid2pcard.update(dict(zip(pids, len(pids) * [pcardname])))
        return pid2pcard

    def pid2pcard(self):
        """
        return a dictionnary mapping Property ID <PID> to cardname <PCARD> {PID: PCARD}

        >>> dic = reg.mesh.pid2pcard()
        >>> dic == {4: 'PCOMP', 5: 'PCOMP', 6: 'PCOMP', 7: 'PCOMP',
        ...         8: 'PBUSH', 9: 'PBUSH', 10: 'PBUSH', 1: 'PSHELL', 2: 'PSHELL'}
        True

        """
        return self._pid2pcard

    @cached_property
    def _pid2eids(self):
        """return a dictionnary mapping PID to a set of concerned elements"""
        _pid2eids = defaultdict(set)
        for eid, pid in self.eid2pid().items():
            _pid2eids[pid].add(eid)
        return {pid: frozenset(eids) for pid, eids in _pid2eids.items()}

    def pid2eids(self, pids=None):
        if pids is None:
            return self._pid2eids
        return {pid: eids for pid, eids in self._pid2eids.items() if pid in pids}

    def pid2bbox(self):
        """return a dict mapping pid to 6 items tuple (xmin, ymin, zmin, xmax, ...)"""
        pid2bbox = {}
        allgrids = self.coords(incsys=0, asdf=True)[["X", "Y", "Z"]]
        for pid, gids in self.pid2gids().items():
            tokens = []
            grids = allgrids.loc[gids]
            tokens += grids.min().to_list()
            tokens += grids.max().to_list()
            pid2bbox[pid] = tuple(tokens)
        return pid2bbox

    def get_eid_bbox(self, eid):
        """non-cached bbox calculation for element. This calls caches:
        * grid array (via query_id)
        * eid2gids
        """
        grids = self.reg.container["bulk"]["GRID"]
        card = self.reg.container["bulk"][self.get_eid_cardname(eid)]
        _ = card.query_id_fast(eid, columns=card.gids_header)
        gids = _[card.gids_header[0]], _[card.gids_header[1]]
        ar2 = grids.query_id_fast(gids, columns=("X1", "X2", "X3"))
        xyz2 = np.array(list(ar2.values())).T
        res2 = np.hstack((np.min(xyz2, axis=0), np.max(xyz2, axis=0)))
        # ar = grids.query_id(gids)
        # xyz = ar.view((ar.dtype[2], len(ar.dtype.names)))[:, 2:5]
        # res = np.hstack((np.min(xyz, axis=0), np.max(xyz, axis=0)))
        # breakpoint()
        return res2

    @cached_property
    def _eid2bbox(self):
        grids = pd.DataFrame(
            self.reg.container["bulk"]["GRID"].array[["ID", "X1", "X2", "X3"]]
        )
        elements = pd.Series(self.reg.mesh.eid2gids(), name="gid")
        # elements.explode(0)
        df = elements.explode().to_frame().set_index("gid", append=True)
        df.index.names = ["eid", "gid"]
        df.reset_index(level=0, inplace=True)
        df = df.merge(grids, left_index=True, right_on="ID")
        df.index.names = ["gid"]
        df = df.reset_index().set_index("eid").sort_index().reset_index()
        df = df[["eid", "X1", "X2", "X3"]]
        bboxes = df.groupby("eid")
        mins = bboxes.min()
        maxs = bboxes.max()
        df = pd.merge(
            mins, maxs, left_index=True, right_index=True, suffixes=("_min", "_max")
        )
        return df

    def eid2bbox(self):
        return self._eid2bbox

    @cached_property
    def _pid2gids(self):
        _pid2gids = {}
        for pid, eids in self.pid2eids().items():
            gids = self.eid2gids(eids=eids, asbunch=True)
            _pid2gids[pid] = gids
        return _pid2gids

    def pid2gids(self, pids=None):
        if pids is None:
            return self._pid2gids
        return {pid: gids for pid, gids in self._pid2gids.items() if pid in pids}

    @cached_property
    def _gid2pids(self):
        ret = defaultdict(set)
        for pid, gids in self.pid2gids().items():
            for gid in gids:
                ret[gid].add(pid)
        return {gid: frozenset(pids) for gid, pids in ret.items()}

    def gid2pids(self, gids=None):
        if gids is None:
            return self._gid2pids.copy()
        return {gid: pids for gid, pids in self._gid2pids.items() if gid in gids}

    @cached_property
    def _pid2thk(self):
        """return a mapping {pid: thk}"""
        pid2thk = {}
        pcards = self.reg.summary[PROPERTY]
        for cardname, cardobj in self.reg.container[BULK.title].items():
            if cardname not in pcards or not hasattr(cardobj, "thk"):
                continue
            thks = pd.Series(**cardobj.thk).round(12).to_dict()
            pid2thk.update(thks)
        return pid2thk

    def pid2thk(self, pids=None):
        """return a mapping {pid: thk}

        >>> reg.mesh.pid2thk()
        {1: 0.09, 2: 0.126, 4: 0.5, 5: 0.375, 6: 0.5, 7: 0.75}
        >>> reg.mesh.pid2thk(pids=(1, 4, -1))
        {1: 0.09, 4: 0.5}
        """
        pid2thk = self._pid2thk
        if pids:
            return {k: v for k, v in pid2thk.items() if k in pids}
        return pid2thk

    def meetic(
        self,
        eids=None,
        gids=None,
        pids=None,
        cards=None,
        samepid=None,
        samecard=None,
        anglemax=None,
        min_paths=1,
        debug_eid=None,
        **kwargs,
    ):
        """filter out meetic dictionnary based on multiple criteria"""
        m = self._meetic.copy()

        def debug():
            if not debug_eid:
                return
            md = m[(m.eid1 == debug_eid) | (m.eid2 == debug_eid)]
            mc = md[["eid1", "eid2", "gid"]].groupby(["eid1", "eid2"]).count()
            print("nbpossibilities: %s" % len(md))
            print(mc)
            print("--------------------")

        # --------------------------------------------------------------------
        # build query
        queries = []
        if eids:
            queries.append("(eid1 in @eids | eid2 in @eids)")
        if gids:
            queries.append("(gid in @gids)")
        if pids:
            queries.append("(pid1 in @pids | pid2 in @ pids)")
            # m = m[(m.pid_1.isin(pids)) | (m.pid_2.isin(pids))]
        if cards:
            queries.append("(card1 in @cards | card2 in @ cards)")
            # m = m[(m.card_1.isin(cards)) | (m.card_2.isin(cards))]
        if anglemax:
            queries.append("(angle <= @anglemax)")
            # m = m[m.angle <= anglemax]
        if samecard is not None:
            assert isinstance(samecard, bool)
            queries.append("(same_card == @samecard)")
            # m = m[m.same_card == samecard]
        if samepid is not None:
            assert isinstance(samepid, bool)
            queries.append("(same_pid == @samepid)")
            # m = m[m.same_pid == samepid]
        for col, crit in kwargs.items():
            # m = m[m[col] == crit]
            queries.append(f'({col} == "{crit}")')
        query = " & ".join(queries)
        if query:
            logging.debug(f'query meetic with "{query}"')
            m = m.query(query)
        if min_paths > 1:
            mg = m[["eid1", "eid2", "gid"]].groupby(["eid1", "eid2"]).count()
            mg = mg[mg.gid >= min_paths]
            m = m.set_index(["eid1", "eid2"]).loc[mg.index]
            m = m.reset_index().set_index(["gid", "pathid"]).sort_index()
        return m

    def autogroup(self, meeticmod):
        """
        create groups of elements based on connectivity described by meeticmod
        """
        edges = {frozenset(edge) for edge in meeticmod[["eid1", "eid2"]].values}
        if HAS_NX:
            # if networkx is installed, use it
            G = nx.Graph()
            G.add_edges_from(edges)
            grps = [G.subgraph(c) for c in nx.connected_components(G)]
            grps = set(frozenset(g.nodes) for g in grps)
            return grps
        else:
            # home made
            return edges

    @cached_property
    def _meetic(self):
        """create an associativity array

        gid: eid1 | eid2
        """
        meetic = {}
        g2s = self._gid2eids
        for gid, eids in g2s.items():
            # sort eids such as eid1<eid2
            eids = sorted(list(eids))
            for i, pair in enumerate(combinations(eids, 2)):
                meetic[gid, i] = pair
        # --------------------------------------------------------------------
        # debug eid
        # debug_eid = 6107
        # for gid, eids in meetic.items():
        #     if debug_eid in eids:
        #         __import__('pdb').set_trace()
        # --------------------------------------------------------------------
        pairs = np.array(list(meetic.values()))
        gids = np.array(list(meetic.keys()))
        gidspairs = np.hstack((gids, pairs))
        df = pd.DataFrame(
            gidspairs, columns=["gid", "pathid", "eid1", "eid2"]
        )  # .set_index(['gid', 'pathid'])
        _df = df.copy()
        # --------------------------------------------------------------------
        # collect cards data
        e2d = self._eid2data.copy()
        df = pd.merge(df, e2d, left_on="eid1", right_index=True)
        df = pd.merge(df, e2d, left_on="eid2", right_index=True, suffixes=("1", "2"))
        df["same_card"] = df.card1 == df.card2
        df["same_pid"] = df.pid1 == df.pid2
        df["same_dim"] = df.dim1 == df.dim2
        # --------------------------------------------------------------------
        # eid2pcard.
        # Merge using `how='left'` since some elements (RBEx) do not have properties
        e2pc = pd.Series(self._eid2pcard, name="pcard").to_frame()
        df = pd.merge(df, e2pc, left_on="eid1", right_index=True, how="left")
        df = pd.merge(
            df, e2pc, left_on="eid2", right_index=True, suffixes=("1", "2"), how="left"
        )
        df["same_pcard"] = df.pcard1 == df.pcard2
        # --------------------------------------------------------------------
        # calculate angle...
        nn = self.normals()
        df["angle"] = angle_0_pi(
            nn.loc[df.eid1].values, nn.loc[df.eid2].values, range_0_pi=True
        )
        return df.sort_index()

    def free_edges(self, eids=None, _check_eids_as_2d=True):
        """
        Return free edges data for provided ``eids``. If ``eids`` is None, calculate
        free edges for the whole model.

        the returned data consists in a tuple (``free_edges``, ``free_edges_gids``)
        where:

        * ``free_edges`` is a ``frozenset`` of N ``frozensets``, where N is the number of free edges
        * ``free_edges_gids`` is a single frozenset of all the nodes on free edges.


        Only 2D elements are taken into account. If 0d, 1d or 3d elements are passed in
        the ``eids`` parameter, they are silently skipped.

        :param eids: element IDs
        :type eids: any iterable of integers OR ``None``

        :returns: tuple of ``frozensets``

        >>> fedges, fedges_gids = reg.mesh.free_edges()
        >>> fedges
        <networkx.classes.graph.Graph ...
        >>> fedges_gids
        {1, 2, 3, 4, ...
        >>> # providing ``eids`` restrict free edges to provided element IDs:
        >>> fedges, gids =reg.mesh.free_edges(eids=(1,))
        >>> gids
        {13, 12, 5, 15}
        >>> fedges.edges()
        EdgeView([(12, 5), (12, 15), (5, 13), (15, 13)])
        >>> fedges.edges()[(5, 12)]
        {'eid': 1, 'eids': frozenset({1})}
        """
        if not eids:
            _eids2d = self.eids_by_dim("2d")
            eids = _eids2d
        elif _check_eids_as_2d:
            _eids2d = self.eids_by_dim("2d")
            eids = set(eids) & _eids2d

        eid2gids = self.eid2gids(eids, keep_order=True)
        gid2eids = self.gid2eids(self.eid2gids(eids, asbunch=True))
        edges = []
        _eids = {}
        _all_eids_on_fedge = {}
        for eid, gids in eid2gids.items():
            for g1, g2 in zip(gids, gids[1:] + [gids[0]]):
                fs = frozenset((g1, g2))
                # if g1 > g2:
                #     g1, g2 = g2, g1
                # fs = (g1, g2)
                edges.append(fs)
                # keep track of element ID generating the current free edge
                # since we will only keep SINGLE free edge, it's safe to store the data
                # as dictionnary
                _eids[fs] = eid
                # `eid` would miss triangulate element having one single node
                # on free edge. Correct it by collecting all eids attached
                # to the free edge
                # _all_eids_on_fedge[fs] = self.gid2eids(fs, asbunch=True) & eids
                _all_eids_on_fedge[fs] = (gid2eids[g1] | gid2eids[g2]) & eids
        # --------------------------------------------------------------------
        # find single edges
        fedges = nx.Graph()
        # generator of networkx-friendly tuples (g1, g2, {'eid': eid})
        single = (
            (*k, {"eid": _eids[k], "eids": _all_eids_on_fedge[k]})
            for k, v in Counter(edges).items()
            if v == 1
        )
        fedges.add_edges_from(single)
        fedges_gids = set(fedges.nodes())
        return fedges, fedges_gids

    def to_grouped_vtk(
        self,
        filename=None,
        eids=None,
        title="",
        include_nastran_ids=True,
        exclude_cards=(),
        include_cards=(),
        # grouping options:
        grp_model=True,
        grp_cards=True,
        grp_properties=True,
        user_groups=None,
    ):
        all_groups = {}
        # =================================================================
        # Whole model
        # =================================================================
        if grp_model:
            grid, gids_vtk2nas, eids_vtk2nas = self.to_vtk(
                title="whole model",
            )
            # for lcid, df in forces.groupby(level="subcaseid"):
            #     _df = df.loc[lcid]
            #     _df = _df.reindex(_id_order_by_vtk2nas(gids_vtk2nas))
            #     _forces = list(df.T.to_dict(orient="list").values())
            #     grid.point_data[f"force-LCID{lcid}"] = _forces
            all_groups["whole model"] = grid
        # =================================================================
        # model cards
        # =================================================================
        if grp_cards:
            cards = {}
            for card, eids in self.card2eids().items():
                grid, gids_vtk2nas, eids_vtk2nas = self.to_vtk(
                    title=f"{card}S",
                    eids=eids,
                )
                cards[card + "S"] = grid
            if len(cards) > 0:
                all_groups["element cards"] = pv.MultiBlock(cards)
        # =================================================================
        # model Properties
        # =================================================================
        if grp_properties:
            _pids = defaultdict(list)
            pids = {}
            for eid, pid in self.eid2pid().items():
                _pids[pid].append(eid)
            for pid, eids in _pids.items():
                grid_pid, gids_vtk2nas, eids_vtk2nas = self.to_vtk(
                    title=f"{pids}S",
                    eids=eids,
                )
                pids[f"PID{pid}"] = grid_pid
            if len(pids) > 0:
                all_groups["element PIDs"] = pv.MultiBlock(pids)
        # =====================================================================
        # user defined groups
        # assuming user_groups={'<groupname>': [eids]}
        # =====================================================================
        if user_groups:
            pids = {}
            for groupname, eids in user_groups.items():
                _pid, gids_vtk2nas, eids_vtk2nas = self.to_vtk(eids=eids)
                pids[groupname] = _pid
            if len(pids) > 0:
                all_groups["user def"] = pv.MultiBlock(pids)

        # put everything in the same .vtm file
        meshes = pv.MultiBlock(all_groups)
        if filename:
            _fname = os.path.abspath(filename)
            meshes.save(_fname, binary=not ascii)
        else:
            return meshes

    def to_vtk(
        self,
        filename=None,
        eids=None,
        title="",
        include_nastran_ids=True,
        exclude_cards=(),
        include_cards=(),
    ):
        """export VTK grid object, optionally as subset by providing
        expected elements `eids`.
        """
        if not ISPYVISTA or not ISVTK:
            raise RuntimeError("PyVista not installed")
        if not include_cards:
            include_cards = cards_mod.collection()
        exclude_cards = set(exclude_cards) | cards_mod.collection() - set(include_cards)
        eid2card = self._eid2card.copy()
        # --------------------------------------------------------------------
        # get elements of interest (if `eids` is None, get all elements)
        _eids = self.eid2gids(keep_order=False)
        _eids = {
            eid: _gids
            for eid, _gids in _eids.items()
            if eid2card[eid] not in exclude_cards
        }
        SUBMESH = False
        if eids:
            SUBMESH = True
            _eids = {eid: _gids for eid, _gids in _eids.items() if eid in eids}
        eids = np.array(list(_eids.keys()))
        # --------------------------------------------------------------------
        # get ALL gids and coordinates
        _gids = set()
        for eid, _gids_per_eid in _eids.items():
            _gids |= _gids_per_eid
        gids, coords, csys = self.coords(gids=_gids, asdf=False, incsys=0)
        # --------------------------------------------------------------------
        # iterate over each card having `to_vtk` method
        cardnames = self.reg.summary["element"] - exclude_cards

        cell_types = []
        cells = []
        cell_types = []
        cell_eids = []
        gids_vtk2nas = {}
        eids_vtk2nas = {}
        cards = []

        # --------------------------------------------------------------------
        # put RBEs as as last cards since they create "fake" elements
        # --------------------------------------------------------------------
        fake_elts_cards = ("RBE2", "RBE3")
        cardnames = [c for c in cardnames if c not in fake_elts_cards] + [
            c for c in fake_elts_cards if c in cardnames
        ]

        for cardname in cardnames:
            if SUBMESH:
                card = self.reg.container[BULK.title][cardname].subset(eids=eids)
            else:
                card = self.reg.container[BULK.title][cardname]
            # if card in not included in subset...
            if not hasattr(card, "to_vtk"):
                logging.info(f"export to VTK: skip {cardname} (no `to_vtk` method)")
                continue
            if len(card) == 0:
                logging.info(f"export to VTK: skip {cardname} (empty set)")
                continue

            vtkdata = card.to_vtk(nasgids=gids)
            cells.append(vtkdata["cells"])
            cell_types += vtkdata["cell_types"]
            cell_eids += vtkdata["eids"]
            cards += vtkdata["card"]
        # --------------------------------------------------------------------
        # map VTK elements indices to NASTRAN element IDs
        eids_vtk2nas = dict(zip(range(len(cell_eids)), cell_eids))
        # ----------------------------------------------------------------
        # map VTK node indices to NASTRAN node IDs
        gids_vtk2nas = dict(zip(range(len(gids)), gids))

        cells = np.concatenate(cells)
        cell_types = [getattr(vtk, attr) for attr in cell_types]
        cell_types = np.array(cell_types)
        nastran_cards = np.array(cards)
        grid = pv.UnstructuredGrid(cells, cell_types, coords)
        if include_nastran_ids:
            grid["NASgid"] = [gids_vtk2nas[i] for i in range(grid.n_points)]
            grid["NAScard"] = [nastran_cards[i] for i in range(grid.n_cells)]
            grid["NASeid"] = [eids_vtk2nas[i] for i in range(grid.n_cells)]
            grid["PID"] = [self._eid2pid[eid] for eid in grid["NASeid"]]
        if filename:
            fname = os.path.abspath(os.path.splitext(filename)[0] + ".vtu")
            grid.save(fname)
            print(f"saved {fname}")
            return
        return grid, gids_vtk2nas, eids_vtk2nas

    # def _to_gmsh_physical_names(self, data):
    #     """
    #     calculate GMSH physical names for:
    #         * properties
    #         * materials
    #         *
    #     """
    #     breakpoint()

    def to_gmsh(
        self,
        filename=None,
        entities_field="pid",
        eid2data=None,
        gid2data=None,
        lcids=None,
    ):
        """dumps registry to GMSH mesh file"""
        # =====================================================================
        # build eids_data
        # =====================================================================
        eids_data = self.eid2data().copy()
        eids_data["_dimint_"] = eids_data["dim"].str.slice(0, 1).astype(int)
        eids_data = eids_data[
            ["_dimint_", "pid", "card", "const"]
        ].dropna()  # discard CONM2, RBE2, etc...
        # cardname 2 gmsh element type
        c2t = pd.Series(
            {
                cname: getattr(self.reg.bulk[cname], "gmsh_eltype", None)
                for cname in self.reg.bulk
            },
            name="gmsh_eltype",
        )
        eids_data = eids_data.join(c2t, on="card", how="left")
        eids_data["gmsh_eltype"] = eids_data["gmsh_eltype"].astype(int)
        eids_data = eids_data.fillna("None")
        # ---------------------------------------------------------------------
        # eventually merge with additional eids_data.
        # eid2data being a dict of dict {:'newfield': {<eid>: <value>}}
        eids_data = eids_data.merge(
            pd.DataFrame(eid2data), left_index=True, right_index=True, how="left"
        )
        eids_data = eids_data.rename(
            columns={entities_field: "_entity_", "gmsh_eltype": "_gmsh_eltype_"}
        )
        # ---------------------------------------------------------------------
        # prepare eids2entity and entities2physicalnames
        colnames = [c for c in eids_data.columns if not c.startswith("_")]
        for colname in eids_data.columns:
            if colname in ("_dimint_", "_gmsh_eltype_"):
                continue
            _colname = colname
            if colname == "_entity_":
                _colname = entities_field
            eids_data.loc[:, colname] = f"{_colname}{GMSH_STR_SEP}" + eids_data[
                colname
            ].astype(str)

        entities2physicalnames = eids_data.reset_index().groupby(
            ["_dimint_", "_gmsh_eltype_", "_entity_"]
        )
        entities2physicalnames = entities2physicalnames.agg(
            dict(zip(colnames, [lambda x: set(x.tolist())] * len(colnames)))
        ).stack()
        entities2physicalnames.name = "_physicalnames_"
        entities2physicalnames = (
            entities2physicalnames.reset_index()
            .drop(columns=["level_3"])
            .set_index("_entity_")
        )
        eids2entity = eids_data[["_dimint_", "_gmsh_eltype_", "_entity_"]]
        # =====================================================================
        # build gids_data.
        # no _entity_ for them : one entity per GID
        # =====================================================================
        gids_data = self.coords(asdf=True)[["X", "Y", "Z"]]
        gids_data = gids_data.join(self.boundaries["dof"].astype(str))
        if gid2data is not None:
            gids_data = gids_data.merge(
                gid2data, left_index=True, right_index=True, how="left"
            )
        gids_data["_entity_"] = f"GID{GMSH_STR_SEP}" + gids_data.index.astype(str)
        for colname in gids_data.columns:
            if colname in ("X", "Y", "Z", "_entity_"):
                continue
            gids_data.loc[:, colname] = f"{colname}{GMSH_STR_SEP}" + gids_data[
                colname
            ].astype(str)
        gids_data["_dimint_"] = 0
        gids_data["_gmsh_eltype_"] = -1  # avoid NaN to keep column as integer
        colnames = [
            c for c in gids_data.columns if not c.startswith("_") and c not in "XYZ"
        ]
        gids2entity = gids_data[["_dimint_", "_gmsh_eltype_", "_entity_"]]
        _df = gids_data.reset_index().set_index(
            ["_dimint_", "_gmsh_eltype_", "_entity_"]
        )[colnames]
        _df = (
            _df.groupby(["_dimint_", "_gmsh_eltype_", "_entity_"])
            .agg(dict(zip(colnames, [lambda x: set(x.tolist())] * len(colnames))))
            .stack()
        )
        _df.name = "_physicalnames_"
        _df = _df.reset_index().drop(columns=["level_3"]).set_index("_entity_")
        entities2physicalnames = pd.concat((entities2physicalnames, _df))
        # =====================================================================
        # save _params
        # =====================================================================
        self._params = {
            "entities2physicalnames": entities2physicalnames,
            "gids2entity": gids2entity,
            "eids2entity": eids2entity,
            "eids_data": eids_data,
            "gids_data": gids_data,
        }
        lines = ["$MeshFormat", "4.1 0 8", "$EndMeshFormat"]
        # self._to_gmsh_prepro()
        lines += self._to_gmsh_physical_names()
        lines += self._to_gmsh_entities()
        lines += self._to_gmsh_nodes()
        lines += self._to_gmsh_elements()
        if lcids:
            if lcids is True:
                breakpoint()
            if isinstance(lcids, int):
                lcids = (lcids,)
            for lcid in lcids:
                lines += self._to_gmsh_loading(lcid)
        txt = "\n".join(lines)
        if filename:
            with open(filename, "w") as fh:
                fh.write(txt)
            return filename
        # delattr(self, "_params")
        return txt

    def _to_gmsh_physical_names(self):
        _physicalnames = {}

        lines = ["$PhysicalNames"]
        # =====================================================================
        # elements physical names
        # =====================================================================
        __physicalnames = set()
        for _entity_, _df in self._params["entities2physicalnames"].iterrows():
            __physicalnames |= {
                (_df["_dimint_"], _entity_),
                (_df["_dimint_"], next(iter(_df["_physicalnames_"]))),
            }
        ptag = 1
        null = f"{GMSH_STR_SEP}nan"
        for dimint, name in __physicalnames:
            if name.endswith(null):
                continue
            lines.append(f'{dimint} {ptag} "{name}"')
            _physicalnames[(dimint, name)] = ptag
            ptag += 1
        lines.insert(1, str(len(lines) - 1))
        lines.append("$EndPhysicalNames")
        self._params["physicalnames"] = _physicalnames
        return lines

    def _to_gmsh_entities(self):
        dim2count = {0: 0, 1: 0, 2: 0, 3: 0}
        _entities = {}
        entity_tag = 1
        tail = f"{GMSH_STR_SEP}nan"
        physicalnames = (
            self._params["entities2physicalnames"]
            .reset_index()
            .set_index(["_dimint_", "_entity_"])
        ).sort_index()
        pn2 = self._params["physicalnames"]
        # ---------------------------------------------------------------------
        # nodes entities
        gids_data = self._params["gids_data"]
        for gid, row in gids_data.iterrows():
            _entity_ = row["_entity_"]
            # if (
            #     _entity_.endswith("tail")
            #     or (0, _entity_) not in physicalnames["_physicalnames_"].index
            # ):
            #     continue
            also = list(physicalnames["_physicalnames_"].loc[0, _entity_])
            grp_ids = [next(iter(i)) for i in also]
            grp_ids = [i for i in grp_ids if not i.endswith(tail)]
            if grp_ids:
                grp_ids = [str(pn2[(0, grpid)]) for grpid in grp_ids]
            # if not grp_ids:
            #     continue
            dim2count[0] += 1
            _entities[(0, f"GID{GMSH_STR_SEP}{gid}")] = {
                "entity_tag": entity_tag,
                "bbox": row[["X", "Y", "Z"]].tolist(),
                "gid": gid,
                "physical_tags": grp_ids,
            }
            entity_tag += 1
        # ---------------------------------------------------------------------
        # elements entities
        eids_data = self._params["eids_data"].reset_index()

        for (dim, entity_value), df in eids_data.groupby(["_dimint_", "_entity_"]):
            if entity_value.endswith(tail):
                continue
            dim2count[dim] += 1
            eids = set(df.eid)
            gids = self.eid2gids(eids=eids, asbunch=True)
            xyz = self.coords(asdf=True).loc[list(gids)][["X", "Y", "Z"]]
            bbox = xyz.min().tolist() + xyz.max().tolist()
            # grp_ids = [self._params["physicalnames"][(dim, entity_value)]]
            grp_ids = [entity_value]
            also = list(physicalnames["_physicalnames_"].loc[(dim, entity_value)])
            grp_ids += [next(iter(i)) for i in also]
            if grp_ids:
                grp_ids = [str(pn2[(dim, grpid)]) for grpid in grp_ids]
            # if dim > 0:
            #     breakpoint()
            _entities[(dim, entity_value)] = {
                "entity_tag": entity_tag,
                "bbox": bbox,
                "gids": gids,
                "eids": eids,
                "physical_tags": grp_ids,
            }
            entity_tag += 1
        # =====================================================================
        # dumping entities
        # =====================================================================
        lines = ["$Entities", " ".join(map(str, dim2count.values()))]
        for (dim, entity_value), entity_data in _entities.items():
            physical_tags = entity_data["physical_tags"]
            row = (
                [entity_data["entity_tag"]]
                + entity_data["bbox"]
                + [len(physical_tags)]
                + physical_tags
                + [0]
            )

            line = " ".join(map(str, row))
            lines.append(line)
        lines.append("$EndEntities")
        self._params["entities"] = _entities
        return lines

    def _to_gmsh_nodes(self):
        allgrids = self._params["gids_data"][["X", "Y", "Z"]]
        numEntityBlocks = 0
        numNodes = len(allgrids)
        minNodeTag = min(allgrids.index)
        maxNodeTag = max(allgrids.index)
        # iterate over entity_ids
        gid2entity_name = self._params["gids_data"]["_entity_"].to_dict()
        entities_data = self._params["entities"]
        dim = 0
        lines = ["$Nodes"]
        dummy_0ds = []
        for gid, _entity_ in gid2entity_name.items():
            entity_data = entities_data[(dim, _entity_)]
            xyz = entity_data["bbox"]
            lines.append(f"{dim} {entity_data['entity_tag']} 0 1\n{gid}")
            lines.append(" ".join(list(map(str, xyz))))
            numEntityBlocks += 1
            dummy_0ds.append({"entity_tag": entity_data["entity_tag"], "gid": gid})
        # ---------------------------------------------------------------------
        # dummy 0-D element at node's place
        lines.insert(1, f"{numEntityBlocks} {numNodes} {minNodeTag} {maxNodeTag}")
        lines.append("$EndNodes")
        self._params["dummy_0ds"] = dummy_0ds
        return lines

    def _to_gmsh_elements(self):
        eids_data = self._params["eids_data"]
        numEntityBlocks = 0
        numElements = len(eids_data) + len(self._params["dummy_0ds"])
        minElementTag = min(eids_data.index)
        maxElementTag = max(eids_data.index) + len(self._params["dummy_0ds"])
        entities_data = self._params["entities"]
        out = BytesIO()
        # iterate over entity_ids
        tail = f"{GMSH_STR_SEP}nan"
        for (dimint, eltype, entity_value, card), df in eids_data.groupby(
            ["_dimint_", "_gmsh_eltype_", "_entity_", "card"]
        ):
            if entity_value.endswith(tail):
                continue
            entity_data = entities_data[(dimint, entity_value)]
            out.write(
                f"{dimint} {entity_data['entity_tag']} {eltype} {len(df)}\n".encode()
            )
            card = card[5:]
            _data = pd.DataFrame(self.reg.bulk[card].array)
            nodes = _data.set_index("EID")[self.reg.bulk[card].gids_header]
            nodes = nodes[nodes.index.isin(df.index)].reset_index()
            np.savetxt(out, nodes, fmt="%d")
            numEntityBlocks += 1
        # also dummy 0d elements
        startat = max(eids_data.index) + 1
        for new_eid, dummy in enumerate(self._params["dummy_0ds"], start=startat):
            out.write(
                f"0 {dummy['entity_tag']} 15 1\n{new_eid} {dummy['gid']}\n".encode()
            )
            numEntityBlocks += 1

        lines = ["$Elements"]
        lines.append(f"{numEntityBlocks} {numElements} {minElementTag} {maxElementTag}")
        lines += out.getvalue().decode().strip("\n").split("\n")
        lines.append("$EndElements")
        return lines

    def _to_gmsh_loading(self, lcid):
        lcid_title = (
            f"{lcid}:" + self.reg.container["cases"][f"SUBCASE {lcid}"]["SUBTITLE"]
        )
        df_forces = (
            pd.DataFrame(self.reg.container["bulk"]["FORCE"].array)
            .set_index(["SID", "G"])[["N1", "N2", "N3"]]
            .reset_index("G")
        )
        lines = [
            "$NodeData",
            1,
            f'"{lcid_title}"',
            1,
            0.0,
            3,
            0,
            3,
            f"{len(df_forces.loc[lcid])}",
        ]
        eids_data = df_forces.to_csv(sep=" ", header=False, index=False)
        lines += eids_data.split("\n")
        lines.append("$EndNodeData")
        return map(str, lines)

    def expand(
        self,
        eids,
        by_cards=None,
        by_dims=None,
        by_shapes=None,
        by_eids=None,
        new_only=False,
    ):
        """
        Given a set of elements ``eids``, increase this set by surrounding
        elements, eventually restricted by cards, dim or shape.

        None or Only one of ``by_card``, ``by_dim`` or ``by_shape`` parameter
        shall be passed.

        :param eids: set of element to expand.
        :type eids: sequence of integers

        :param by_cards: *optional* sequence of cards to search for
        :type by_cards: sequence of strings

        :param by_dims: *optional* sequence of dims to search for
        :type by_dims: sequence of strings

        :param by_shapes: *optional* sequence of shapes to search for
        :type by_shapes: sequence of strings

        :param by_eids: *optional* sequence of eids to search for
        :type by_eids: sequence of integers

        :returns: set of elements eids

        >>> # expand whatever the connected elements:
        >>> reg.mesh.expand(eids=(1,2)) == frozenset({1, 2, 3, 11139, 4, 5, 7, 8, 9, 6})
        True
        >>> # expand, but only on CBUSH:
        >>> reg.mesh.expand(eids=(1,2), by_cards=('CBUSH',))
        frozenset({1, 2, 11139})
        >>> # expand, but only on 1D elements
        >>> reg.mesh.expand(eids=(1,2), by_dims=('1d',))
        frozenset({1, 2, 11139})
        >>> reg.mesh.expand(eids=(1,2), by_shapes=('line',))
        frozenset({1, 2, 11139})
        >>> # expand, but only using elements provided
        >>> # this is use full to prepare a more complex expand
        >>> # for example, expanding, but only using small 1d elements:
        >>> df = reg.mesh.eid2data()
        >>> small_1d = df[(df['length'] <= 0.001) & df['card'].isin(('CBUSH', 'RBE2'))]
        >>> reg.mesh.expand(eids=(1,2), by_eids=small_1d.index.tolist())
        frozenset({1, 2})
        >>> reg.mesh.expand(eids=(1,2), by_eids=[], new_only=True)
        frozenset()
        """
        eids = set(eids)
        gids = self.eid2gids(eids=eids, asbunch=True)
        # get elements using those nodes
        expanded_eids = self.gid2eids(gids=gids, asbunch=True)
        expanded_eids -= eids  # keep only new elements
        # --------------------------------------------------------------------
        # excluding by criteria
        if by_cards:
            expanded_eids -= {
                eid
                for eid, card in self.eid2card(expanded_eids).items()
                if card not in by_cards
            }
        elif by_dims:
            expanded_eids -= {
                eid
                for eid, card in self.eid2dim(expanded_eids).items()
                if card not in by_dims
            }
        elif by_shapes:
            expanded_eids -= {
                eid
                for eid, card in self.eid2shape(expanded_eids).items()
                if card not in by_shapes
            }
        elif by_eids is not None:
            expanded_eids &= set(by_eids)
        if new_only:
            return frozenset(expanded_eids)
        return frozenset(eids | expanded_eids)

    # ========================================================================
    # constraints & loading
    # ========================================================================

    @cached_property
    def load_combination(self):
        """return LOAD cards as DataFrame"""
        cards = self.reg.container["bulk"]["LOAD"]
        if not cards:
            return
        loads = pd.DataFrame(cards.array)
        gridsets = cards.carddata["load_factors"]
        df = pd.concat({i: pd.DataFrame(d) for i, d in enumerate(gridsets)})
        df.index.names = ["load_factorsID", "#"]
        df = df.rename(columns={"S": "Si", "L": "Li"})
        df = df.reset_index()
        merged = loads.merge(
            df, how="outer", left_on="load_factorsID", right_on="load_factorsID"
        )
        merged = merged.drop(columns=["load_factorsID", "#"])
        return merged.set_index("SID")

    @cached_property
    def boundaries(self):
        """return dictionnary mapping nodes to constraint DOF
        >>> reg.mesh.boundaries()
                  dof  sid source
        gid
        12508     123  290   SPC1
        12509     123  290   SPC1
        12510     123  290   SPC1
        12511     123  290   SPC1
        12516  123456   -1   GRID
        12517  123456   -1   GRID
        """
        # --------------------------------------------------------------------
        # getting SPC1
        spc1 = pd.DataFrame(self.reg.container["bulk"]["SPC1"].array)
        #    SID    C  spc1_gridsetID
        # 0  290  123               0
        # 1  290  123               1
        # 2  290  123               2
        # 3  290  123               3
        gridsets = self.reg.container["bulk"]["SPC1"].carddata["spc1_gridset"]
        df = pd.concat({i: pd.DataFrame(d) for i, d in enumerate(gridsets)})
        df.index.names = ["spc1_gridsetID", "#"]
        df.reset_index(level=-1, inplace=True)
        df = spc1.merge(df, right_index=True, left_on="spc1_gridsetID")[
            ["SID", "C", "G"]
        ]
        df = df.reset_index(drop=True)
        df["source"] = "SPC1"
        # --------------------------------------------------------------------
        # getting permanent constraints nodes "SD"
        nodes = pd.DataFrame(self.reg.container["bulk"]["GRID"].array)
        nodes = nodes.dropna(subset=["PS"])[["ID", "PS"]]
        nodes.columns = ["G", "C"]
        nodes["source"] = "GRID"
        #          ID  CP      X1     X2   X3  CD        PS  SEID
        # 4392  12516   0  372.45 -42.28  0.0   0  123456.0   NaN
        # 4393  12517   0  363.95 -42.28  0.0   0  123456.0   NaN

        # df = pd.concat((df, nodes))
        df = pd.concat((df, nodes), axis=0)
        df.C = df.C.astype(int)
        df = df[["C", "G", "SID", "source"]]  #  ensure columns order
        # df.SID = df.SID.astype(int)  # SID may be NaN if source is "GRID"
        df.columns = ["dof", "gid", "sid", "source"]
        df.sid = df.sid.fillna(-1).astype(int)
        # --------------------------------------------------------------------
        return df.reset_index(drop=True).set_index("gid")


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
