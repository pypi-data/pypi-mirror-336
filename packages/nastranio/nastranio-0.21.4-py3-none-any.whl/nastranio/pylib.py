"""
Python fallbacks when clib.pyx not compiled
"""

import string

# ==============================================================================
# autoconvert
# ==============================================================================
ALPHA = set(string.ascii_letters)
DIGITS = set(string.digits)
NULLSET = set()
ESET = set("Ee")


def autoconvert_array(fields):
    res = [autoconvert(f) for f in fields]
    return res


def autoconvert(field):
    field = field.strip()
    if not field:
        # ------------------------------------------------------
        # Empty
        return None
    # ------------------------------------------------------------------------
    # simple continuation lines
    if field == "+":
        return "+"
    s = set(field)
    if "." not in s and s & ALPHA == NULLSET:
        return int(field)

    if "." in s and ((s - ESET) & ALPHA == NULLSET):
        # ------------------------------------------------------
        # Real
        # special NASTRAN format +/-XXX+/-YYY = +/-XXXE+/-YYY
        i = field.rfind("+")
        if i > 0 and field[i - 1] != "E":
            return float(field[:i] + "E" + field[i:])
        i = field.rfind("-")
        if i > 0 and field[i - 1] != "E":
            return float(field[:i] + "E" + field[i:])
        # regular float
        return float(field)
    else:
        # ------------------------------------------------------
        # string
        return field
