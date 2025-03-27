#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Helpers to write NASTRAN cards
"""
from math import floor, log10


def nbrows_by_fields(fields):
    """return the number of rows that would be used to write provided
    fields dictionnary

    example: if two fields only are provided #17 and #23,
    we need to write row 11->20 and 21->30

    >>> nbrows_by_fields({17: 'robert', 23:'toto'})
    2
    """
    keys = fields.keys()
    kmax = max(keys)
    kmin = min(keys)
    # if kmin would be <=10, nb of rows would be
    rowid_min = (kmin - 1) // 10
    rowid_max = (kmax - 1) // 10
    return (rowid_max - rowid_min) + 1


def mantexp(f):
    """return the mantissa and exponent of a number as a tuple
    >>> mantexp(-2.3)
    (-2.3, 0)
    >>> mantexp(-1.123456789E-12)
    (-1.123456789, -12)
    """
    exponent = int(floor(log10(abs(f)))) if f != 0 else 0
    return f / 10**exponent, exponent


def _trans_float(value, field_length=8):
    """
    return float's string representation in NASTRAN way. Try to reduce as much
    as possible the string's length while keeping precision.


    >>> _trans_float(15)
    '15.'
    >>> _trans_float(-15.999)
    '-15.999'
    >>> _trans_float(15.9999999999999999999)
    '16.'
    >>> _trans_float(12345678)
    '1.2346+7'
    >>> _trans_float(123456789)
    '1.2346+8'
    >>> _trans_float(-0.123456789)
    '-.123457'
    >>> _trans_float(-0.999999999997388)
    '-1.'
    >>> _trans_float(0.999999999997388)
    '1.'
    >>> _trans_float(270000.0)
    '2.7000+5'
    """
    exponent = ""
    available_chars = field_length
    available_digits = field_length
    # ========================================================================
    # non-exponential numbers:
    #   * 0
    #   * range: ]-100000, -0.001]
    #   * range: [0.001, 100000[
    # ========================================================================
    # simple cases
    if value == 0:
        return "0."
    elif -1 < value < -0.001:
        # we loose two digits: "-."
        tpl = "{{:.{}f}}".format(field_length - 2)
        s = tpl.format(value)
        # return *minus* sign (s[0], skip leading "0" (s[1]) and trailing 0)
        if s[1] == "0":
            return s[0] + s[2:].rstrip("0")
        return s[0] + s[1:].rstrip("0")
    elif 0.001 < value < 1:
        # leading "0" can be omitted
        tpl = "{{:.{}f}}".format(field_length - 1)
        s = tpl.format(value)
        if s[0] == "0":
            return s[1:].rstrip("0")
        return s[0:].rstrip("0")

    # ------------------------------------------------------------------------
    # more complex stuff
    elif -100000 < value <= -1:
        # negative number. We loose one digit for the '-' sign and one for the '.'
        available_digits -= (
            len(str(int(value))) + 1
        )  # loose digits for integer part and dot
        tpl = "{{0:.{}f}}".format(available_digits)
        return tpl.format(value).rstrip("0")
    elif 1 <= value < 100000:
        available_digits -= (
            len(str(int(value))) + 1
        )  # loose digits for integer part and dot
        tpl = "{{0:.{}f}}".format(available_digits)
        return tpl.format(value).rstrip("0")
    # ========================================================================
    # exponential numbers:
    #   * range: -0.001, 0.001     # (excl. borns) small numbers
    #   * range: -inf,  -100000    # (incl. borns) big negative numbers
    #   * range: 100000, +inf      # (incl. borns) big negative numbers
    # ========================================================================
    else:
        # use exponent notation
        mantissa, exponent = mantexp(value)
        available_chars = field_length - len(str(exponent)) - 2
        if exponent > 0:
            available_chars -= 1
        if mantissa < 0:
            available_chars -= 1
        E_format = "{{mantissa:.{}f}}{{exponent:+d}}".format(available_chars)
        return E_format.format(mantissa=mantissa, exponent=exponent)


def _trans_int(val, field_length):
    """
    simply returns the integer as string (`str(val)`), except when resulting
    length is more than allowed length. In this latter case, an exception is raised.

    >>> _trans_int(1, 8)
    '1'
    """
    s = str(val)
    if len(s) <= field_length:
        return s
    # as per NASTRAN documentation, there shouldn't be any interger
    # whose length is longer than field's length
    raise ValueError(
        "encountered integer (%d) wider than %d chars" % (val, field_length)
    )


def trans(val, field_length=8):
    """translate field to NASTRAN compliant 8-characters fields

    >>> checks = ((6250, '6250'),
    ...           (0.0, '0.'),
    ...           (6250.0, '6250.'),
    ...           (-0.123456789, "-.123457"),
    ...           (0.123456789, ".1234568"),
    ...           (0.0023148, '.0023148'),
    ...           (-1.987654e-12, '-1.99-12'),
    ...           (None, ""))
    >>> err = []
    >>> for val, exp in checks:
    ...     if trans(val) != exp:
    ...         err.append((val, exp, trans(val)))
    >>> err
    []

    """
    if val is None:  # return blank field
        res = ""
    elif isinstance(val, float):
        res = _trans_float(val, field_length=field_length)
    elif isinstance(val, int):
        res = _trans_int(val, field_length=field_length)
    else:
        res = val
    # assert len(res) <= field_length
    return res


class DefaultDict(dict):
    def __missing__(self, key):
        return ""


def fields_to_card(fields, leading="", sep=""):
    """convert a single card dictionnary of fields to nastran card"""
    # the `fields` dict should look like:
    # {'fn1': str1, 'fn2': str2, ..., 'fn12': str3}
    if len(fields["fn1"]) + len(leading) + len(sep) > 8:
        raise ValueError('leading length is too long to fit with "%s"' % fields["fn1"])
    tpl = (
        "{leading}{{fn%d:{w1}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}"
        "{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:>{w}}}{sep}{{fn%d:{w}}}{sep}"
    )
    _d = {
        "w1": 8 - len(leading) - len(sep),
        "w": 8 - len(sep),
        "leading": leading,
        "sep": sep,
    }
    tpl = tpl.format(**_d)
    # clean fields
    for fieldcode, fieldvalue in fields.copy().items():
        if not fieldvalue:
            fields.pop(fieldcode)
    # calculate the number of rows:
    fieldmax = max([int(k[2:]) for k in fields.keys()])
    nb_rows = fieldmax // 10 + 1
    # populate continuation fields
    for fnb in range(2, fieldmax):
        if fnb % 10 == 0 or (fnb - 1) % 10 == 0:
            fields["fn%d" % fnb] = "+"
    # prepare the multiline template
    tpls = []
    for i in range(0, nb_rows):
        ix = range(1 + i * 10, 11 + i * 10)
        tpls.append(tpl % tuple(ix))
    tpl = "\n".join(tpls)
    lines = tpl.format_map(fields).split("\n")
    lines = [l.strip() for l in lines]
    return lines


def get_field(field_nb):
    """simply return `field_nb` when `field_nb` is not a continuation field nb (10, 11,
    20, 21, etc.). Otherwise return next available field

    >>> get_field(1)
    1
    >>> get_field(11)
    12
    >>> get_field(14)
    14
    >>> get_field(10)
    12
    >>> get_field(11)
    12
    >>> get_field(21)
    22
    """
    if field_nb == 1:
        return 1
    if field_nb % 10 == 0:
        return field_nb + 2
    if (field_nb - 1) % 10 == 0:
        return field_nb + 1
    return field_nb


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
