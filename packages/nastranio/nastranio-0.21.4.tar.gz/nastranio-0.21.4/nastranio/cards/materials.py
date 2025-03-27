"""
NASTRAN material Cards Collection
"""

import logging
import re
from collections import defaultdict

from nastranio.cardslib import SimpleCard
from nastranio.decorators import material


@material
class MAT1(SimpleCard):
    """
    Isotropic Material Property Definition
    Defines the material properties for linear isotropic materials.

    ref: NX Nastran 12 Quick Reference Guide 15-2 (p.1968)
    """

    COMMENTS_KEY = "Material"

    TABLE = """
    | 1    | 2   | 3  | 4  | 5     | 6   | 7 | 8    | 9  | 10 |
    |------+-----+----+----+-------+-----+---+------+----+----|
    | MAT1 | MID | E  | G  | NU    | RHO | A | TREF | GE |    |
    |      | ST  | SC | SS | MCSID |     |   |      |    |    |
    """

    DEFAULTS = {
        "G": None,
        "NU": None,
        "RHO": 0.0,
        "A": 0.0,
        "TREF": 0.0,
        "GE": None,
        "ST": None,
        "SC": None,
        "SS": None,
        "MCSID": None,
    }


@material
class MAT8(SimpleCard):
    """
    Shell Element Orthotropic Material Property Definition
    Defines the material property for an orthotropic material for isoparametric shell
    elements.

    ref: NX Nastran 12 Quick Reference Guide 15-19 (p.1985)
    """

    COMMENTS_KEY = "Material"

    TABLE = """
    | 1    | 2   | 3   | 4    | 5    | 6   | 7   | 8   | 9   | 10 |
    |------+-----+-----+------+------+-----+-----+-----+-----+----|
    | MAT8 | MID | E1  | E2   | NU12 | G12 | G1Z | G2Z | RHO |    |
    |      | A1  | A2  | TREF | Xt   | Xc  | Yt  | Yc  | S   |    |
    |      | GE  | F12 | STRN |      |     |     |     |     |    |

    """
