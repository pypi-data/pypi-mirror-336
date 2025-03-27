"""
NASTRAN loading cards collection.

This include loading and constraints, therfore, GRIDS cards
"""

import logging
import re
from collections import defaultdict
from pprint import pprint

import numpy as np
import pandas as pd
from numtools.vgextended import loc_array

from nastranio.cardslib import SimpleCard, SimpleCyclingCard
from nastranio.decorators import boundary, cached_property, loading_type


@loading_type()
class GRAV(SimpleCard):
    """
    Acceleration or Gravity Load
    Defines acceleration vectors for gravity or other acceleration loading.

    ref: NX Nastran 12 Quick Reference Guide 14-55 (p.1921)

    >>> grav = GRAV()
    >>> bulk = ["GRAV           1       0      1.     -9.      0.      0.",
    ...         "GRAV           1       0      1.     -9.      0.      0.       5"]
    >>> for b in bulk: grav.parse(b)
    >>> pprint(grav.export_data()['main'])
    {'A': [1.0, 1.0],
     'CID': [0, 0],
     'MB': [0, 5],
     'N1': [-9.0, -9.0],
     'N2': [0.0, 0.0],
     'N3': [0.0, 0.0],
     'SID': [1, 1]}
    """

    TABLE = """
| 1    | 2   | 3   | 4 | 5  | 6  | 7  | 8  | 9 | 10 |
|------+-----+-----+---+----+----+----+----+---+----|
| GRAV | SID | CID | A | N1 | N2 | N3 | MB |   |    |
    """
    DEFAULTS = {"CID": 0, "MB": 0}


@loading_type("nodal")
class FORCE(SimpleCard):
    """
    Static Force
    Defines a static concentrated force at a grid point by specifying a vector.

    ref: NX Nastran 12 Quick Reference Guide 14-10 (p.1876)
    """

    TABLE = """
    | 1     | 2   | 3 | 4   | 5 | 6  | 7  | 8  | 9 | 10 |
    |-------+-----+---+-----+---+----+----+----+---+----|
    | FORCE | SID | G | CID | F | N1 | N2 | N3 |   |    |
    """
    DEFAULTS = {"cid": 0, "N1": 0.0, "N2": 0.0, "N3": 0.0}


@loading_type("nodal")
class MOMENT(SimpleCard):
    """
    Static Moment
    Defines a static concentrated moemnt at a grid point by specifying a vector.

    ref: NX Nastran 12 Quick Reference Guide 15-127 (p.2093)
    """

    TABLE = """
    | 1      | 2   | 3 | 4   | 5 | 6  | 7  | 8  | 9 | 10 |
    |--------+-----+---+-----+---+----+----+----+---+----|
    | MOMENT | SID | G | CID | M | N1 | N2 | N3 |   |    |
    """
    DEFAULTS = {"cid": 0, "N1": 0.0, "N2": 0.0, "N3": 0.0}


@loading_type()
class LOAD(SimpleCyclingCard):
    """
    Static Force
    Defines a static concentrated force at a grid point by specifying a vector.

    ref: NX Nastran 12 Quick Reference Guide 14-90 (p.1956)
    """

    TABLE = """
    | 1    | 2   | 3  | 4      | 5  | 6  | 7  | 8  | 9  | 10 |
    |------+-----+----+--------+----+----+----+----+----+----|
    | LOAD | SID | S  | S1     | L1 | S2 | L2 | S3 | L3 |    |
    |      | S4  | L4 | -etc.- |    |    |    |    |    |    |
    """
    REPEATED_DATA_NAME = "FACTORS"


@loading_type("elemental")
class PLOAD4(SimpleCard):
    """
    Pressure Load on Shell and Solid Element Faces
    Defines a pressure load on a face of a CHEXA, CPENTA, CTETRA, CPYRAM,
    CTRIA3, CTRIA6, CTRIAR, CQUAD4, CQUAD8, or CQUADR element.

    ref: NX Nastran 12 Quick Reference Guide 16-164 (p.2394)

    Alternate format (using "THRU") not taken into account.
    """

    TABLE = """
    | 1      | 2   | 3   | 4  | 5  | 6  | 7  | 8  | 9      | 10 |
    |--------+-----+-----+----+----+----+----+----+--------+----|
    | PLOAD4 | SID | EID | P1 | P2 | P3 | P4 | G1 | G3orG4 |    |
    |        | CID | N1  | N2 | N3 |    |    |    |        |    |
    """


@boundary
class SPC1(SimpleCyclingCard):
    """
    Single-Point Constraint, Alternate Form
    Defines a set of single-point constraints.

    ref: NX Nastran 12 Quick Reference Guide 17-174 (p.2648)

    >>> spc1 = SPC1()
    >>> bulk = ["SPC1         290     123   12508",
    ...         "SPC1         292     123      12",
    ...         "SPC1         291  123456   12509       2       3       4       5"]
    >>> for b in bulk: spc1.parse(b)
    >>> pprint(spc1.export_data()['main'])  # doctest: +NORMALIZE_WHITESPACE
    {'C': [123, 123, 123456], 'SID': [290, 292, 291], 'spc1_gridsetID': [0, 1, 2]}
    >>> pprint(spc1.export_data()['spc1_gridset'])  # doctest: +NORMALIZE_WHITESPACE
    [[{'G': 12508}],
     [{'G': 12}],
     [{'G': 12509}, {'G': 2}, {'G': 3}, {'G': 4}, {'G': 5}]]
    """

    REPEATED_DATA_NAME = "GRIDSET"
    TABLE = """
    | 1    | 2   | 3  | 4  | 5      | 6  | 7  | 8  | 9  | 10 |
    |------+-----+----+----+--------+----+----+----+----+----|
    | SPC1 | SID | C  | G1 | G2     | G3 | G4 | G5 | G6 |    |
    |      | G7  | G8 | G9 | -etc.- |    |    |    |    |    |
    """


@boundary
class GRID(SimpleCard):
    """
    Grid Point
    Defines the location of a geometric grid

    ref: NX Nastran 12 Quick Reference Guide 14-60 (p.1926)
    """

    TABLE = """
        | 1    | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9    | 10 |
        |------+----+----+----+----+----+----+----+------+----|
        | GRID | ID | CP | X1 | X2 | X3 | CD | PS | SEID |    |
    """
    DEFAULTS = {
        "CP": 0,
        "CD": 0,
        "PS": None,
        "SEID": None,
        "X1": 0.0,
        "X2": 0.0,
        "X3": 0.0,
    }
    XID_FIELDNAME = "ID"

    def to_vtk(self, **kwargs):
        """return grids as VTK legacy format"""
        from io import StringIO

        fh = StringIO()
        msg = ["POINTS %d double" % len(self)]
        coords = self.coords()[1]
        np.savetxt(fh, coords, **kwargs)
        fh.seek(0)
        msg += fh.readlines()
        return msg

    def coords(self, incsys=None, csysreg=None, gids=None, asdf=False):
        """
        return two numpy arrays: one vector of eids and one 3xN matrix of coordinates
        """
        cdefined = self.array[["ID", "CP", "X1", "X2", "X3"]]  # coordinates as defined
        _gids = cdefined["ID"]
        xyz = np.vstack((cdefined["X1"], cdefined["X2"], cdefined["X3"])).T
        csys = cdefined["CP"]
        if gids:
            if not isinstance(gids, (list, np.ndarray)):
                gids = list(gids)
        # ====================================================================
        # calculate coordinates in requested CSYS
        # ====================================================================
        if incsys:  # not None and not 0
            if incsys == -1:  # way for _translate_grids_to_0 to bypass
                incsys = 0
            _initial_gids = _gids.copy()
            # which points are not concerned?
            nop = csys == incsys
            nop_gids, _gids = _gids[nop], _gids[~nop]
            nop_xyz, xyz = xyz[nop], xyz[~nop]
            nop_csys, csys = csys[nop], csys[~nop]
            origins = set(csys)  # this will define how many change we will perform
            for origin_csys in origins:
                csys_obj = csysreg[origin_csys]
                # search all the points defined in origin_csys
                which = csys == origin_csys
                c_gids, c_xyz, c_csys = _gids[which], xyz[which], csys[which]
                c_xyz = csys_obj.export_vertices(c_xyz, to_csys=incsys)
                c_csys.fill(incsys)
                # nothing to change to c_gids
                nop_xyz = np.vstack((nop_xyz, c_xyz))
                nop_gids = np.hstack((nop_gids, c_gids))
                nop_csys = np.hstack((nop_csys, c_csys))
            xyz, _gids, csys = nop_xyz, nop_gids, nop_csys
            # ----------------------------------------------------------------
            # sort arrays as initially sorted
            positions = loc_array(_initial_gids, _gids)
            np.put(_gids, positions, _gids)
            np.put(xyz[:, 0], positions, xyz[:, 0])
            np.put(xyz[:, 1], positions, xyz[:, 1])
            np.put(xyz[:, 2], positions, xyz[:, 2])
            np.put(csys, positions, csys)

        if gids:
            mask = np.isin(_gids, gids, assume_unique=True)
            _gids = _gids[mask]
            xyz = xyz[mask]
            csys = csys[mask]

        if len(set(csys)) > 1:
            logging.warning("return coords in different systems")

        if not asdf:
            return _gids, xyz, csys
        else:
            data = np.insert(xyz, 0, csys, axis=1)
            df = pd.DataFrame(data, columns=["csys", "X", "Y", "Z"], index=_gids)
            df.csys = df.csys.astype(int)
            df.index.names = ["gid"]
            return df


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
