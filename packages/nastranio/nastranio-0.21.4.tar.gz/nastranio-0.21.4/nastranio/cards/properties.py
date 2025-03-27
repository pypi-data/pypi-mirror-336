"""
NASTRAN property Cards collection
"""

import logging
import re
from collections import defaultdict
from pprint import pprint

import numpy as np

from nastranio.cardslib import (
    ComplexCard,
    RepeatedRowsCard,
    SimpleCard,
    SimpleCyclingCard,
)
from nastranio.decorators import cached_property, fem_property


@fem_property
class PCOMP(SimpleCyclingCard):
    """
    Layered Composite Element Property.
    Defines the properties of an n-ply composite material laminate.

    ref: NX Nastran 12 Quick Reference Guide 16-97 (p.2327)


    >>> pcomp = PCOMP()
    >>> pcomp.append_fields_list(
    ...              [      1001, None, 0.00361, None,  None,  None, None, None,  '+',
    ...               '+',  1002, 0.018,    0.0, 'YES', 1003, 0.339,  0.0, 'YES', '+',
    ...               '+',  1009, 0.018,    5.0, 'YES'])
    >>> pcomp.append_fields_list(
    ...              [      1002, None, 0.005, None,  None,  None, None, None,  '+',
    ...               '+',  1002, 0.018,    0.0, 'YES', 1003, 0.339,  None, 'YES', '+',
    ...               '+',  1009, 0.018,    5.0, 'YES'])
    >>> # check main data:
    >>> pprint(pcomp.carddata['main'])  # doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {'FT': [None, None],
                 'GE': [None, None],
                 'LAM': [None, None],
                 'NSM': [0.00361, 0.005],
                 'PID': [1001, 1002],
                 'SB': [None, None],
                 'TREF': [None, None],
                 'Z0': [None, None],
                 'pcomp_layupID': [0, 0]})
    >>> # check LAYUPs creation. Both cards come with the same layout values. Therefore
    >>> # only one LAYUP (made of three plies) is created:
    >>> pprint(pcomp.carddata['pcomp_layup'])  # doctest: +NORMALIZE_WHITESPACE
    [[{'MID': 1002, 'SOUT': 'YES', 'T': 0.018, 'THETA': 0.0},
      {'MID': 1003, 'SOUT': 'YES', 'T': 0.339, 'THETA': 0.0},
      {'MID': 1009, 'SOUT': 'YES', 'T': 0.018, 'THETA': 5.0}]]
    """

    DIM = "2d"
    REPEATED_DATA_NAME = "layup"
    TABLE = """
| 1     | 2    | 3  | 4      | 5     | 6      | 7    | 8      | 9     | 10 |
|-------+------+----+--------+-------+--------+------+--------+-------+----|
| PCOMP | PID  | Z0 | NSM    | SB    | FT     | TREF | GE     | LAM   |    |
| ""    | MID1 | T1 | THETA1 | SOUT1 | MID2   | T2   | THETA2 | SOUT2 |    |
| ""    | MID3 | T3 | THETA3 | SOUT3 | -etc.- |      |        |       |    |
"""
    DEFAULTS = {
        "NSM": 0.0,
        "Z0": None,
        "SB": None,
        "FT": None,
        "TREF": None,
        "GE": None,
        "LAM": None,
    }
    REPEATED_DEFAULTS = {"THETA": 0.0, "SOUT": "NO"}
    COMMENTS_KEY = "Property"

    @cached_property
    def thk(self):
        """return a dict of thicknesses"""
        # calculate thicknesses for all layups
        layup_thks = {}
        for layID, data in enumerate(self.carddata["pcomp_layup"]):
            ts = [ply["T"] for ply in data]
            layup_thks[layID] = sum(ts)
        # map to PIDS
        thks = {
            pid: layup_thks[lay]
            for pid, lay in zip(
                self.carddata["main"]["PID"], self.carddata["main"]["pcomp_layupID"]
            )
        }
        return {
            "data": np.array(list(thks.values())),
            "index": np.array(list(thks.keys())),
            "name": "pid2thk",
        }

    @cached_property
    def pid2mids(self):
        """This ovverides the default "pid2mids" defined in `cardslib` module"""
        ret = {}

        for ix, pid in enumerate(self.carddata["main"]["PID"]):
            ret[pid] = set()
            layup_id = self.carddata["main"]["pcomp_layupID"][ix]
            layups = self.carddata["pcomp_layup"][layup_id]
            for layup in layups:
                ret[pid].add(layup["MID"])
            ret[pid] = frozenset(ret[pid])
        return ret


@fem_property
class PBAR(SimpleCard):
    """
    Simple Beam Property.
    Defines the properties of a simple beam element (CBAR entry).

    ref: NX Nastran 12 Quick Reference Guide 16-32 (p.2262)
    """

    DIM = "1d"
    COMMENTS_KEY = "Property"
    TABLE = """
| 1    | 2   | 3   | 4   | 5  | 6  | 7  | 8   | 9  | 10 |
|------+-----+-----+-----+----+----+----+-----+----+----|
| PBAR | PID | MID | A   | I1 | I2 | J  | NSM |    |
| ""   | C1  | C2  | D1  | D2 | E1 | E2 | F1  | F2 |
| ""   | K1  | K2  | I12 |    |    |    |     |    |
"""

    DEFAULTS = {
        "K1": 0.0,
        "K2": 0.0,
        "A": 0.0,
        "I1": 0.0,
        "I2": 0.0,
        "I12": 0.0,
        "J": 0.0,
        "NSM": 0.0,
        "C1": 0.0,
        "D1": 0.0,
        "E1": 0.0,
        "F1": 0.0,
        "C2": 0.0,
        "D2": 0.0,
        "E2": 0.0,
        "F2": 0.0,
    }


@fem_property
class PSHEAR(SimpleCard):
    """
    SHEAR Panel Property
    Defines the propertires of a shear panel (CSHEAR entry).

    ref: NX Nastran 12 Quick Reference Guide 16-208 (p.2438)


    """

    DIM = "2d"
    COMMENTS_KEY = "Property"
    TABLE = """
| 1      | 2   | 3    | 4    | 5    | 6  | 7   | 8  | 9  | 10 |
|--------+-----+------+------+------+----+-----+----+----+----|
| PSHEAR | PID | MID  | T    | NSM  | F1 | F2  |    |    |    |
"""
    DEFAULTS = {
        "NSM": 0.0,
        "F1": 0.0,
        "F2": 0.0,
    }

    @cached_property
    def thk(self):
        """return a dict of thicknesses"""
        thks = {
            pid: thk
            for pid, thk in zip(
                self.carddata["main"]["PID"], self.carddata["main"]["T"]
            )
        }
        # thks -> {1: 0.09, 203: 1.9}
        return {
            "data": np.array(list(thks.values())),
            "index": np.array(list(thks.keys())),
            "name": "pid2thk",
        }


@fem_property
class PSHELL(SimpleCard):
    """
    Shell Element Property
    Defines the membrane, bending, transverse shear, and coupling properties of thin
    shell elements.

    ref: NX Nastran 12 Quick Reference Guide 16-210 (p.2440)
    """

    DIM = "2d"
    COMMENTS_KEY = "Property"
    TABLE = """
| 1      | 2   | 3    | 4    | 5    | 6        | 7    | 8    | 9   | 10 |
|--------+-----+------+------+------+----------+------+------+-----+----|
| PSHELL | PID | MID1 | T    | MID2 | 12I/T**3 | MID3 | TS/T | NSM |    |
|        | Z1  | Z2   | MID4 |      |          |      |      |     |    |
"""
    DEFAULTS = {
        "12I/T**3": None,
        "TS/T": None,
        "NSM": 0.0,
        "Z1": None,
        "Z2": None,
        "MID4": None,
    }

    @cached_property
    def thk(self):
        """return a dict of thicknesses"""
        thks = {
            pid: thk
            for pid, thk in zip(
                self.carddata["main"]["PID"], self.carddata["main"]["T"]
            )
        }
        # thks -> {1: 0.09, 203: 1.9}
        return {
            "data": np.array(list(thks.values())),
            "index": np.array(list(thks.keys())),
            "name": "pid2thk",
        }


@fem_property
class PROD(SimpleCard):
    """
    Rod Property.

    Defines the properties of a rod element (CROD entry).

    ref: NX Nastran 12 Quick Reference Guide 16-206 (p.2436)
    """

    DIM = "1d"
    COMMENTS_KEY = "Property"
    TABLE = """
    | 1    | 2   | 3   | 4 | 5 | 6 | 7   | 8 | 9 | 10 |
    |------+-----+-----+---+---+---+-----+---+---+----|
    | PROD | PID | MID | A | J | C | NSM |   |   |    |
    """

    DEFAULTS = {"C": 0, "NSM": 0}


@fem_property
class PBUSH(ComplexCard):
    """
    Generalized Spring-and-Damper Property
    Defines the nominal property values for a generalized spring-and-damper structural
    element.

    ref: NX Nastran 12 Quick Reference Guide 16-83 (p.2800)
    """

    DIM = "1d"
    COMMENTS_KEY = "Property"
    TABLE = """
    | 1     | 2   | 3     | 4   | 5   | 6   | 7   | 8   | 9   | 10 |
    |-------+-----+-------+-----+-----+-----+-----+-----+-----+----|
    | PBUSH | PID | "K"   | K1  | K2  | K3  | K4  | K5  | K6  |    |
    |       |     | "B"   | B1  | B2  | B3  | B4  | B5  | B6  |    |
    |       |     | "GE"  | GE1 | GE2 | GE3 | GE4 | GE5 | GE6 |    |
    |       |     | "RCV" | SA  | ST  | EA  | ET  |     |     |    |
    """

    DEFAULTS = {
        "C": 0,
        "NSM": 0,
        '"K"': "K",
        "K1": None,
        "K2": None,
        "K3": None,
        "K4": None,
        "K5": None,
        "K6": None,
        '"B"': "B",
        "B1": None,
        "B2": None,
        "B3": None,
        "B4": None,
        "B5": None,
        "B6": None,
        '"GE"': "GE",
        "GE1": None,
        "GE2": None,
        "GE3": None,
        "GE4": None,
        "GE5": None,
        "GE6": None,
        '"RCV"': "RCV",
        "SA": None,
        "ST": None,
        "EA": None,
        "ET": None,
    }

    def clean_sparams(self, sparams):
        """remove"""
        Kfields = set((f"K{i}" for i in range(1, 6)))
        Ks = set((sparams[Ki] for Ki in Kfields))
        if Ks == {None}:
            Kfields.add('"K"')
            for field in Kfields:
                sparams.pop(field)
        Bfields = set((f"B{i}" for i in range(1, 6)))
        Bs = set((sparams[Bi] for Bi in Bfields))
        if Bs == {None}:
            Bfields.add('"B"')
            for field in Bfields:
                sparams.pop(field)
        GEfields = set((f"GE{i}" for i in range(1, 6)))
        GEs = set((sparams[GEi] for GEi in GEfields))
        if GEs == {None}:
            GEfields.add('"GE"')
            for field in GEfields:
                sparams.pop(field)


@fem_property
class PBEAM(RepeatedRowsCard):
    """
    Beam Property
    Defines the properties of a beam element (CBEAM entry). This element may be
    used to model tapered beams.

    ref: NX Nastran 12 Quick Reference Guide 16-48 (p.2278)

    > If SO is “YESA” or “NO”, the third continuation entry, which contains the fields
    > C1 through F2, must be omitted. If SO is “YES”, the continuation for Ci, Di, Ei,
    > and Fi must be the next entry.

    > ...

    > The fourth and fifth continuation entries, which contain fields K1 through
    > N2(B), are optional and may be omitted if the default values are appropriate.
    """

    DIM = "1d"
    COMMENTS_KEY = "Property"
    TABLE = """
    | 1     | 2     | 3      | 4     | 5     | 6     | 7      | 8     | 9      | 10 |
    |-------+-------+--------+-------+-------+-------+--------+-------+--------+----|
    | PBEAM | PID   | MID    | A(A)  | I1(A) | I2(A) | I12(A) | J(A)  | NSM(A) |    |
    |       | C1(A) | C2(A)  | D1(A) | D2(A) | E1(A) | E2(A)  | F1(A) | F2(A)  |    |
    """

    REPEATED_ROWS_TABLE = """
    | 1 | 2  | 3    | 4  | 5  | 6  | 7   | 8  | 9   | 10 |
    |---+----+------+----+----+----+-----+----+-----+----|
    |   | SO | X/XB | A  | I1 | I2 | I12 | J  | NSM |    |
    |   | C1 | C2   | D1 | D2 | E1 | E2  | F1 | F2  |    |
    """

    TRAILING_ROWS_TABLE = """
    | 1 | 2     | 3     | 4     | 5     | 6      | 7      | 8     | 9     | 10 |
    |---+-------+-------+-------+-------+--------+--------+-------+-------+----|
    |   | K1    | K2    | S1    | S2    | NSI(A) | NSI(B) | CW(A) | CW(B) |    |
    |   | M1(A) | M2(A) | M1(B) | M2(B) | N1(A)  | N2(A)  | N1(B) | N2(B) |
    """

    REPEATED_ROWS_NAME = "stations"
    TRIGGER_REPEATED_ON = str
    SKIP_NEXT_ROW_ON = ("SO", ("YESA", "NO"))
    DEFAULTS = {"I12(A)": 0.0, "J(A)": 0.0, "NSM(A)": 0.0}


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
