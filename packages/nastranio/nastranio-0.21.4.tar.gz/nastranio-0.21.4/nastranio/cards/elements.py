"""
NASTRAN Elements Cards collection
"""

import logging
import re
from collections import defaultdict
from itertools import chain
from pprint import pprint

import numpy as np
from numtools.vgextended import loc_array

from nastranio.cardslib import ComplexCard, SimpleCard, SimpleCyclingCard
from nastranio.constants import VTKShapes, shapes
from nastranio.decorators import element


@element("0d", shapes.VERTICE)
class CONM2(SimpleCard):
    """
    Concentrated Mass Element Connection, Rigid Body Form
    Defines a concentrated mass at a grid point.


    ref: NX Nastran 12 Quick Reference Guide 12-4 (p.1488)
    """

    TABLE = """
    | 1     | 2   | 3   | 4   | 5   | 6   | 7   | 8  | 9 | 10 |
    |-------+-----+-----+-----+-----+-----+-----+----+---+----|
    | CONM2 | EID | G   | CID | M   | X1  | X2  | X3 |   |    |
    |       | I11 | I21 | I22 | I31 | I32 | I33 |    |   |    |
    """
    DEFAULTS = {"CID": 0}

    GIDS_PATTERN = re.compile("^G$")


@element("1d", shapes.LINE)
class CROD(SimpleCard):
    """
    Rod Element Connection.
    Defines a tension-compression-torsion element.


    ref: NX Nastran 12 Quick Reference Guide 12-120 (p.1604)
    """

    TABLE = """
    | 1    | 2   | 3   | 4  | 5  | 6 | 7  | 8 | 9 | 10 |
    |------+-----+-----+----+----+---+----+---+---+----|
    | CROD | EID | PID | G1 | G2 |   | SM |   |   |    |
    """

    DEFAULTS = {"C": 0, "NSM": 0}


# ============================================================================
# RBE3/RBE2
# ============================================================================


def _cells(cls, nasgids=None):
    """
    return RBE2 and RBE3 element's cell definition.
    """
    gidnames = ["nbpoints", cls.gids_header[0], "G2"]  # ['GN', 'G2']
    cells = [[], [], []]
    eids = cls.carddata["main"][cls.EID_FIELDNAME]
    eid2gids = cls._eid2gids
    # ========================================================================
    # default nasgids and naseids
    # ========================================================================
    if nasgids is None:
        logging.warning("no gids nor eids passed as reference")
        nasgids = list(cls._eid2gids.values())
        nasgids = np.array(sorted(list(chain(*nasgids))))
        naseids = np.array(sorted(list(cls.eid2gids().keys())))
    # -------------------------------------------------------------------------
    # for each element in cards,
    # create a bunch of dummy 2D element per leg, iterating over RBE nodes
    # calculate offset such as we ensure we do not point on existing EID
    faked_eids = []
    # print(cls.eid2gids())
    for eid in eids:
        master_gid = cls.array[np.where(cls.array["EID"] == eid)][cls.gids_header[0]][0]
        slave_gids = eid2gids[eid].copy()
        slave_gids.remove(master_gid)
        nb_fake_elements = len(slave_gids) - 1
        # append number of nodes
        cells[0] += (1 + nb_fake_elements) * [2]
        # ------------------------------------------------------------------------
        # map VTK nodes to NASTRAN nodes
        for slave_gid in slave_gids:
            faked_eids.append(eid)
            gids = [master_gid, slave_gid]
            gids = np.array(gids)
            gix = loc_array(nasgids, gids)
            cells[1].append(gix[0])
            cells[2].append(gix[1])

    payload = {
        "data": np.array(cells).T,
        "index": np.array(faked_eids),
        "columns": gidnames,
    }
    return payload


@element("1d", shapes.MPC)
class RBE3(ComplexCard):
    """
    Interpolation Constraint Element.

    Defines the motion at a reference grid point as the weighted average
    of the motions at a set of other grid points.

    ref: NX Nastran 12 Quick Reference Guide 17-48 (p.2522)
    """

    TABLE = """
    | 1    | 2       | 3     | 4       | 5    | 6    | 7      | 8    | 9      | 10 |
    |------+---------+-------+---------+------+------+--------+------+--------+----|
    | RBE3 | EID     |       | REFGRID | REFC | WT1  | C1     | G1,1 | G1,2   |    |
    |      | -etc.-  | WT2   | C2      | G2,1 | G2,2 | -etc.- | WT3  | C3     |    |
    |      | G3,1    | G3,2  | -etc.-  | WT4  | C4   | G4,1   | G4,2 | -etc.- |    |
    |      | "UM"    | GM1   | CM1     | GM2  | CM2  | GM3    | CM3  |        |    |
    |      |         | GM4   | CM4     | GM5  | CM5  | -etc.- |      |        |    |
    |      | "ALPHA" | ALPHA |         |      |      |        |      |        |    |
    """

    GIDS_PATTERN = re.compile("^REFGRID$")

    def __init__(self, name=None, data=None):
        super().__init__(name, data=data)
        # change self.fields and self.repeated
        self.fields = {fid: fname for fid, fname in self.fields.items() if fid <= 5}
        self.repeated = None
        if "rbe3_wcg" not in self.carddata:
            self.carddata["rbe3_wcg"] = []
        if "rbe3_um" not in self.carddata:
            self.carddata["rbe3_um"] = []

    def eid2gids_complement(self, eid=None, ix=None):
        """retrieve nodes stored in rbe3_wcg data"""
        gids = set()
        for data in self.carddata["rbe3_wcg"][ix]:
            gids |= data["Gi"]
        return gids

    def append_checkin(self, fields):
        """hook triggered right before `append`"""
        # fixed fields go to (including) field#5 "REFC"
        fixed_fields = fields[:4]  # to be parsed as usual
        self._remaining_fields = fields[4:]
        return fixed_fields

    def append_checkout(self, fields):
        """hook triggered right after `append`"""
        WCG_sequences = []
        UM_sequences = []
        buffer = None
        # we begin with WCG sequence
        FLAG = "WCG"
        _sequence = WCG_sequences
        fields = ["_", "_", "_", "_", "_", "_"] + self._remaining_fields

        for field_nb, field in enumerate(fields):
            try:
                next_field = fields[field_nb + 1]
            except:
                next_field = "EoF"
            if field == "_":
                continue
            # ----------------------------------------------------------------
            # skip continuation fields (fields #X0 or fields#X1
            if field_nb % 10 == 0 or (field_nb - 1) % 10 == 0:
                continue
            # ================================================================
            # WCG sequence
            # ================================================================
            if FLAG == "WCG":
                # ------------------------------------------------------------
                # opening a new sub-sequence, and closing the previous one
                # when we meet a float
                if isinstance(field, float):
                    if buffer:
                        # eventually close previous sub-sequence
                        _sequence.append(buffer)
                    buffer = []
                # ------------------------------------------------------------
                # closing the WCG sequence:
                #   * first None field parsed  (end of WCG, but not end of fields)
                #   * meeting "UM" or "ALPHA" flag
                #   * when reaching end of fields (next_field=='EoF')
                if field in ("UM", "ALPHA", None) or next_field == "EoF":
                    if next_field == "EoF":
                        # current field is still good
                        buffer.append(field)
                    # end of WCG current sequence AND also of WCG sequences
                    if buffer:
                        _sequence.append(buffer)
                        buffer = []
                    if field == "UM":
                        FLAG = "UM"
                        _sequence = UM_sequences
                    if field == "ALPHA":
                        FLAG = "ALPHA"
                    continue
                buffer.append(field)
                continue
            # ================================================================
            # UM sequence
            # ================================================================
            elif FLAG == "UM":
                # ------------------------------------------------------------
                # opening a new UM subsequence when buffer's length is two
                if len(buffer) == 2:
                    _sequence.append(buffer)
                    buffer = []
                # field #x9, #x2 are empty, but still in UM sequence
                if field is None:
                    # we theoritically fushed the buffer above, so...
                    assert len(buffer) == 0
                    continue
                # ------------------------------------------------------------
                # closing a UM sequence:
                #   * meeting "ALPHA" flag
                #   * when reaching end of fields (next_field=='EoF')
                if next_field == "EoF":
                    if buffer:
                        if len(buffer) not in (0, 2):
                            assert len(buffer) == 1
                            buffer.append(field)
                        _sequence.append(buffer)
                        buffer = []
                        IS_ALPHA_DEFAULT = True
                        alpha = 0.0
                        break
                if field == "ALPHA":
                    # end of WCG current sequence AND also of WCG sequences
                    if buffer:
                        if len(buffer) != 2:
                            __import__("pdb").set_trace()
                        _sequence.append(buffer)
                        buffer = []
                    if field == "ALPHA":
                        FLAG = "ALPHA"
                    continue
                buffer.append(field)
                continue
            elif FLAG == "ALPHA":
                IS_ALPHA_DEFAULT = False
                alpha = field
                break
        else:
            if buffer:
                _sequence.append(buffer)
            # default value
            IS_ALPHA_DEFAULT = True
            alpha = 0.0
        self.carddata["main"]["ALPHA"].append(alpha)
        # --------------------------------------------------------------------
        # process WCG sequence
        _all_wcg = []
        for weight, dof, *grids in WCG_sequences:
            _all_wcg.append({"W": weight, "C": dof, "Gi": set(grids)})
        if _all_wcg in self.carddata["rbe3_wcg"]:
            ix = self.carddata["rbe3_wcg"].index(_all_wcg)
        else:
            ix = len(self.carddata["rbe3_wcg"])
            self.carddata["rbe3_wcg"].append(_all_wcg)
        self.carddata["main"]["rbe3_wcgID"].append(ix)
        # --------------------------------------------------------------------
        # process UM sequence
        # print(UM_sequences)
        if UM_sequences in self.carddata["rbe3_um"]:
            ix = self.carddata["rbe3_um"].index(UM_sequences)
        else:
            ix = len(self.carddata["rbe3_um"])
            self.carddata["rbe3_um"].append(UM_sequences)
        self.carddata["main"]["rbe3_umID"].append(ix)
        return fields

    def cells(self, nasgids=None):
        """
        return element's cell definition.
        """
        return _cells(self, nasgids)


@element("1d", shapes.MPC)
class RBE2(SimpleCyclingCard):
    """
    Rigid Body Element, Form 2
    Defines a rigid body with independent degrees-of-freedom that are specified at a
    single grid point and with dependent degrees-of-freedom that are specified at an
    arbitrary number of grid points.

    ref: NX Nastran 12 Quick Reference Guide 17-45 (p.2519)

    >>> pb = RBE2()
    >>> pb.append_fields_list([      9, 8, 12, 10, 12, 14, 15, 16, '+',
    ...             '+', 20])
    >>> pb.append_fields_list([     10, 9, 12345, 10, 12, 14, 15, 16, '+',
    ...             '+', 100, 101, 5.])
    >>> pb.append_fields_list([     11, 109, 1245, 10, 12, 14, 15, 16, '+',
    ...             '+', 100, 101])  # no alpha specified. Expect default 0.0
    >>> pprint(pb.carddata['main'])  # doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {'ALPHA': [0.0, 5.0, 0.0],
                 'CM': [12, 12345, 1245],
                 'EID': [9, 10, 11],
                 'GN': [8, 9, 109],
                 'rbe2_gidsetID': [0, 1, 1]})
    >>> pprint(pb.export_data()['rbe2_gidset'])  # doctest: +NORMALIZE_WHITESPACE
    [[{'GM': 10}, {'GM': 12}, {'GM': 14}, {'GM': 15}, {'GM': 16}, {'GM': 20}],
     [{'GM': 10},
      {'GM': 12},
      {'GM': 14},
      {'GM': 15},
      {'GM': 16},
      {'GM': 100},
      {'GM': 101}]]

    """

    REPEATED_DATA_NAME = "gidset"
    TABLE = """
| 1    | 2   | 3   | 4   | 5      | 6     | 7   | 8   | 9   | 10 |
|------+-----+-----+-----+--------+-------+-----+-----+-----+----|
| RBE2 | EID | GN  | CM  | GM1    | GM2   | GM3 | GM4 | GM5 |    |
|      | GM6 | GM7 | GM8 | -etc.- | ALPHA |     |     |     |    |
    """
    DEFAULTS = {"ALPHA": 0.0}
    GIDS_PATTERN = re.compile("^GN$")

    def eid2gids_complement(self, eid=None, ix=None):
        # also include linked nodes
        try:
            compdata = self.carddata[self.REPEATED_DATA_NAME][ix]
        except IndexError as exc:
            logging.error(f"{ix=} out of bounds for {self.REPEATED_DATA_NAME=}")
            raise
        compdata = set([gid for subd in compdata for _, gid in subd.items()])
        return compdata
        # for subset_id, nodes in enumerate(subset):
        #     gidset_nodes[gidset].add(nodes['GM'])
        # eid2gidset = dict(zip(self.carddata['main'][self.EID_FIELDNAME], self.carddata['main']['rbe2_gidsetID']))
        # return eid2gidset

    def nb_nodes(self):
        return 2

    def cells(self, nasgids=None):
        """
        return element's cell definition.
        """
        return _cells(self, nasgids)


@element("2d", shapes.TRIA)
class CTRIA3(SimpleCard):
    """
    Triangular Plate Element Connection
    Defines an isoparametric membrane-bending or plane strain triangular plate element.

    ref: NX Nastran 12 Quick Reference Guide 12-147 (p.1631)
    """

    TABLE = """
    | 1      | 2   | 3     | 4  | 5  | 6  | 7          | 8     | 9 | 10 |
    |--------+-----+-------+----+----+----+------------+-------+---+----|
    | CTRIA3 | EID | PID   | G1 | G2 | G3 | THETA/MCID | ZOFFS |   |    |
    |        |     | TFLAG | T1 | T2 | T3 |            |       |   |    |
    """
    DEFAULTS = {
        "THETA/MCID": 0.0,
        "ZOFFS": None,
        "TFLAG": None,
        "T1": None,
        "T2": None,
        "T3": None,
    }
    MULT_TYPES_FIELDS = {"THETA/MCID": {float: "THETA", int: "MCID"}}


@element("2d", shapes.QUAD)
class CQUAD4(SimpleCard):
    """
    Quadrilateral Plate Element Connection

    Defines an isoparametric membrane-bending or plane strain quadrilateral plate element.

    ref: NX Nastran 12 Quick Reference Guide 12-80 (p.1564)

    >>> cq4 = CQUAD4()
    >>> bulk = ["CQUAD4         1       1       5      12      15      13",
    ...         "CQUAD4         2       4    4524    4537    4569    4547       4",
    ...         "CQUAD4         3       3       1       2       3       4      4."]
    >>> for b in bulk: cq4.parse(b)
    >>> pprint(cq4.export_data()['main']) # doctest: +NORMALIZE_WHITESPACE
    {'EID': [1, 2, 3],
     'G1': [5, 4524, 1],
     'G2': [12, 4537, 2],
     'G3': [15, 4569, 3],
     'G4': [13, 4547, 4],
     'MCID': [None, 4, None],
     'PID': [1, 4, 3],
     'T1': [None, None, None],
     'T2': [None, None, None],
     'T3': [None, None, None],
     'T4': [None, None, None],
     'TFLAG': [None, None, None],
     'THETA': [0.0, None, 4.0],
     'THETA/MCID': [0.0, 4, 4.0],
     'ZOFFS': [None, None, None]}
    """

    TABLE = """
| 1      | 2   | 3     | 4  | 5  | 6  | 7  | 8          | 9     | 10 |
|--------+-----+-------+----+----+----+----+------------+-------+----|
| CQUAD4 | EID | PID   | G1 | G2 | G3 | G4 | THETA/MCID | ZOFFS |    |
|        |     | TFLAG | T1 | T2 | T3 | T4 |            |       |    |
"""
    DEFAULTS = {
        "THETA/MCID": 0.0,
        "ZOFFS": None,
        "TFLAG": None,
        "T1": None,
        "T2": None,
        "T3": None,
        "T4": None,
    }
    MULT_TYPES_FIELDS = {"THETA/MCID": {float: "THETA", int: "MCID"}}


@element("2d", shapes.QUAD)
class CSHEAR(SimpleCard):
    """
    Shear Panel Element Connection

    Defines a Shear Panel element

    ref: NX Nastran 12 Quick Reference Guide 12-126 (p.1610)

    >>> cshear = CSHEAR()
    >>> bulk = ["CSHEAR         1       1       5      12      15      13",
    ...         "CSHEAR         2       4    4524    4537    4569    4547"]
    >>> for b in bulk: cshear.parse(b)
    >>> pprint(cshear.export_data()['main']) # doctest: +NORMALIZE_WHITESPACE
    {'EID': [1, 2],
     'G1': [5, 4524],
     'G2': [12, 4537],
     'G3': [15, 4569],
     'G4': [13, 4547],
     'PID': [1, 4]}
    """

    TABLE = """
| 1      | 2   | 3     | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|--------+-----+-------+----+----+----+----+----+----+----|
| CSHEAR | EID | PID   | G1 | G2 | G3 | G4 |    |    |    |
"""
    DEFAULTS = {}
    THK_PATTERN = None


@element("1d", shapes.LINE)
class CBUSH(SimpleCard):
    """
    Generalized Spring-and-Damper Connection
    Defines a generalized spring-and-damper structural element that may be nonlinear
    or frequency dependent.

    ref: NX Nastran 12 Quick Reference Guide 11-39 (p.1399)
    """

    TABLE = """
    | 1     | 2   | 3    | 4  | 5  | 6     | 7  | 8  | 9   | 10 |
    |-------+-----+------+----+----+-------+----+----+-----+----|
    | CBUSH | EID | PID  | GA | GB | GO/X1 | X2 | X3 | CID |    |
    |       | S   | OCID | S1 | S2 | S3    |    |    |     |    |
    """
    GIDS_PATTERN = re.compile("^G[A|B]$")
    DEFAULTS = {
        "S": None,
        "OCID": None,
        "S1": None,
        "S2": None,
        "S3": None,
        "CID": None,
    }
    MULT_TYPES_FIELDS = {"GO/X1": {float: "X1", int: "GO"}}


@element("1d", shapes.LINE)
class CBAR(SimpleCard):
    """
    Simple Beam Element Connection
    Defines a simple beam element.

    ref: NX Nastran 12 Quick Reference Guide 11-20 (p.1380)
    """

    TABLE = """
    | 1    | 2   | 3   | 4   | 5   | 6     | 7   | 8   | 9   | 10 |
    |------+-----+-----+-----+-----+-------+-----+-----+-----+----|
    | CBAR | EID | PID | GA  | GB  | GO/X1 | X2  | X3  |     |    |
    |      | PA  | PB  | W1A | W2A | W3A   | W1B | W2B | W3B |    |
    """
    MULT_TYPES_FIELDS = {"GO/X1": {float: "X1", int: "GO"}}
    GIDS_PATTERN = re.compile("^G[A|B]$")
    DEFAULTS = {
        "W1A": None,
        "W2A": None,
        "W3A": None,
        "W1B": None,
        "W2B": None,
        "W3B": None,
        "PA": None,
        "PB": None,
    }


@element("1d", shapes.LINE)
class CELAS2(SimpleCard):
    """
    Scalar Spring Property and Connection
    Defines a scalar spring element without reference to a property entry.

    ref: NX Nastran 12 Quick Reference Guide 11-77 (p.1437)
    """

    TABLE = """
    | 1      | 2   | 3 | 4  | 5  | 6  | 7  | 8  | 9 | 10 |
    |--------+-----+---+----+----+----+----+----+---+----|
    | CELAS2 | EID | K | G1 | C1 | G2 | C2 | GE | S |    |
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
