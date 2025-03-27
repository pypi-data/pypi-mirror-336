"""
NASTRAN Axis Cards Collection
"""

import logging
import re
from collections import defaultdict

from nastranio.cardslib import SimpleCard
from nastranio.decorators import axis


# ============================================================================
# axis
# ============================================================================
@axis
class CORD2R(SimpleCard):
    """
    Rectangular Coordinate System Definition, Form 2
    Defines a rectangular coordinate system using the coordinates of three points.


    ref: NX Nastran 12 Quick Reference Guide 12-24 (p.1508)
    """

    TABLE = """
| 1      | 2   | 3   | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|--------+-----+-----+----+----+----+----+----+----+----|
| CORD2R | CID | RID | A1 | A2 | A3 | B1 | B2 | B3 |    |
|        | C1  | C2  | C3 |    |    |    |    |    |    |
    """
    DEFAULT = {"RID": 0}


@axis
class CORD2S(SimpleCard):
    """
    Spherical Coordinate System Definition, Form 2
    Defines a spherical coordinate system using the coordinates of three points.


    ref: NX Nastran 12 Quick Reference Guide 12-26 (p.1510)
    """

    TABLE = """
| 1      | 2   | 3   | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|--------+-----+-----+----+----+----+----+----+----+----|
| CORD2S | CID | RID | A1 | A2 | A3 | B1 | B2 | B3 |    |
|        | C1  | C2  | C3 |    |    |    |    |    |    |
    """
    DEFAULT = {"RID": 0}


@axis
class CORD2C(SimpleCard):
    """
    Cylindrical Coordinate System Definition, Form 2
    Defines a cylindrical coordinate system using the coordinates of three points.


    ref: NX Nastran 12 Quick Reference Guide 12-21 (p.1505)
    """

    TABLE = """
| 1      | 2   | 3   | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|--------+-----+-----+----+----+----+----+----+----+----|
| CORD2C | CID | RID | A1 | A2 | A3 | B1 | B2 | B3 |    |
|        | C1  | C2  | C3 |    |    |    |    |    |    |
    """
    DEFAULT = {"RID": 0}


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
