"""Generic helpers module for developers"""

import datetime as dt
import logging
import os
import time
from collections import defaultdict
from itertools import chain

import numpy as np

try:
    from deepdiff import DeepDiff

    ISDEEPDIFF = True
except ImportError:
    ISDEEPDIFF = False


def project_point_fast(point, ga, gb):
    """
    return a tuple (<projection point>, <`t`>)

    >>> ga = np.array([1.5, 5.5, 0])
    >>> gb = np.array([6, -1.5, 0])
    >>> proj, t= project_point_fast(np.array([9, -1, 0]), ga, gb)

    `proj` is the calcualted projected point:
    >>> proj
    array([ 6.64981949, -2.51083032,  0.        ])

    `t` is the gagb range factor:
        * t<0: projection is 'before' ga
        * t>1, projection is 'after' gb.
    >>> t
    1.144404332129964
    """
    gagb_vector = gb - ga
    t = np.sum((point - ga) * gagb_vector) / np.sum(gagb_vector**2)
    projection = ga + t * gagb_vector
    return projection, t


def project_point(point, ga, gb, strategy="on_extend", return_t=False):
    r"""
    project a point onto a segment [sega, segb] with different strategies:

      * 'strict': calculate projection only if projected point lies between
        ga and gb.
      * 'on_extend': if projection is "outside" of the segment,
        calculate its position on the "extended" segment.
      * 'on_end': if projection is "outside" of the segment,
        calculate the projection as beeing the closest extremity (ga or gb)
        of the theoretical projection.

       + ga
        \
         \
          \   + point
           +
            \
             + gb

    All of those strategies leads to the same result if the projection is
    between [ga, gb]

    >>> ga = np.array([1.5, 5.5, 0])
    >>> gb = np.array([6, -1.5, 0])


    For a point whose projection lies on ga, gb segment, strategy is skipped:

    >>> project_point(np.array([2, 1.5, 0]), ga, gb)
    array([3.46570397, 2.44223827, 0.        ])


    >>> project_point(np.array([9, -1, 0]), ga, gb, strategy='strict')
    Traceback (most recent call last):
        ...
    ValueError: point [9, -1, 0] does not project onto ga-gb line segment

    >>> project_point(np.array([9, -1, 0]), ga, gb, strategy='on_extend')
    array([ 6.64981949, -2.51083032,  0.        ])

    >>> project_point(np.array([9, -1, 0]), ga, gb, strategy='on_end')
    array([ 6. , -1.5,  0. ])
    """
    # distance between ga and gb
    projection, t = project_point_fast(point, ga, gb)
    has_changed = False
    if strategy != "on_extend" and (t > 1 or t < 0):
        if strategy == "strict":
            raise ValueError(
                f"point {point.tolist()} does not project onto ga-gb line segment"
            )
        elif strategy == "on_end":
            # if you need the point to project on line segment between ga and gb or closest point of the line segment
            has_changed = True
            t = max(0, min(1, t))
    if has_changed:
        gagb_vector = gb - ga
        projection = ga + t * gagb_vector
    # distance = np.sum((projection - point) ** 2)
    if not return_t:
        return projection
    return projection, t


def calcdiff(args, exclude_meta=True, **kwargs):
    d1, d2 = args
    if not ISDEEPDIFF:
        msg = "optional DeepDiff lib is not installed"
        raise RuntimeError(msg)
    else:
        if exclude_meta:
            exclude_paths = ["root['meta']", "root['meta']"]
        else:
            exclude_paths = None
        diff = DeepDiff(
            d1,
            d2,
            exclude_regex_paths=[
                r"root\['_.*'\]",
                r"root\[.*'\]\['_.*'\]",
                r"_cached.*",
            ],
            exclude_paths=exclude_paths,
            ignore_type_in_groups=((dict, defaultdict), (list, tuple)),
            ignore_nan_inequality=True,
            **kwargs,
        )
    return diff


class Chronos:
    """
    Easily sequence timing in yout function:

    >>> c = Chronos()
    >>> c.click('hello world')
    hello world: 0:00:00.0...
    >>> time.sleep(0.05)
    >>> c.click('another event')
    another event: 0:00:00.05...
    """

    def __init__(self):
        self._starts = dt.datetime.now()
        self._events = [{"abstime": self._starts, "reltime": 0, "event": "starts"}]

    def click(self, event):
        now = dt.datetime.now()
        reltime = now - self._events[0]["abstime"]
        self._events.append({"abstime": now, "reltime": reltime, "event": event})
        print("%s: %s" % (event, reltime))


# ============================================================================
# numpy structured arrays
# ============================================================================
def dic2array(data):
    """
    Convert a dictionnary to numpy structured array.

    >>> data ={'x': [1.5, 3., 1., 9.7],
    ...        'y': [2.5, 4, None, 5.2],
    ...        'z': [1, 1, 0, 0],
    ...        'w': ['A', 'd', 'B', None],
    ...        'v': [1, 2, None, None],
    ...        'u': [None, None, None, None]
    ...  }
    >>> dic2array(data)
    array([(1.5, 2.5, 1, 'A',  1., nan), (3. , 4. , 1, 'd',  2., nan),
       (1. , nan, 0, 'B', nan, nan), (9.7, 5.2, 0, 'N', nan, nan)],
      dtype=[('x', '<f8'), ('y', '<f8'), ('z', '<i8'), ('w', '<U1'), ('v', '<f8'), ('u', '<f8')])
    >>> import pandas as pd
    >>> pd.DataFrame(dic2array(data))
             x    y  z  w    v   u
    0  1.5  2.5  1  A  1.0 NaN
    1  3.0  4.0  1  d  2.0 NaN
    2  1.0  NaN  0  B  NaN NaN
    3  9.7  5.2  0  N  NaN NaN
    >>> pd.DataFrame(dic2array(data)).dtypes
    x    float64
    y    float64
    z      int64
    w     object
    v    float64
    u    float64
    dtype: object
    """
    values = []
    names = []
    formats = []
    type_None = type(None)
    for k, varray in data.items():
        types = {type(i) for i in varray}
        if str in types:
            formats.append("<U1")
        elif type_None in types or float in types or np.float64 in types:
            formats.append("<f8")
        elif int in types or np.int64 in types:
            formats.append("<i8")
        else:
            breakpoint()
            formats.append("<U1")
        values.append(tuple(varray))
        names.append(k)
    return np.array(list(zip(*values)), dtype={"names": names, "formats": formats})


def dic2array_legacy(data, nb_entries=None, None2NaN=True):
    """
    Convert a dictionnary to numpy structured array.

    >>> data ={'x': [1.5, 3., 1., 9.7],
    ...        'y': [2.5, 4, None, 5.2],
    ...        'z': [1, 1, 0, 0]}
    >>> dic2array(data)
    array([(1.5, 2.5, 1), (3. , 4. , 1), (1. , nan, 0), (9.7, 5.2, 0)],
          dtype=[('x', '<f8'), ('y', '<f8'), ('z', '<i8')])
    >>> data  # data has not been modified
    {'x': [1.5, 3.0, 1.0, 9.7], 'y': [2.5, 4, None, 5.2], 'z': [1, 1, 0, 0]}
    """
    data = {k: v.copy() for k, v in data.items()}
    if not nb_entries:
        krandom = list(data.keys())[0]  # pick-up a random key
        nb_entries = len(data[krandom])
    values = []
    for ix in range(nb_entries):
        col = []
        for fieldname in data.keys():
            val = data[fieldname][ix]
            if val is None and None2NaN:
                val = data[fieldname][ix] = np.NaN
            col.append(val)
        values.append(tuple(col))
    _data = {k: np.array(v) for k, v in data.items()}
    formats = [a.dtype.str for a in _data.values()]
    names = [k for k in data.keys()]

    array = np.array(values, dtype={"names": names, "formats": formats})
    return array


def array2dic(array, astype=None):
    """convert a structured array to regular dictionnary.
    If `astype` is not provided, returned values remain numpy 1D arrays
    >>> data ={'x': [1.5, 3., 1., 9.7],
    ...        'y': [2.5, 4, 3, 5.2],
    ...        'z': [1, 1, 0, 0]}
    >>> array2dic(dic2array(data), astype=list)
    {'x': [1.5, 3.0, 1.0, 9.7], 'y': [2.5, 4.0, 3.0, 5.2], 'z': [1, 1, 0, 0]}
    """
    ret = {}
    if not astype:
        for col in array.dtype.names:
            ret[col] = array[col]
    else:
        for col in array.dtype.names:
            ret[col] = astype(array[col])
    return ret


def bunch_legacy(dic):
    """given a dict {k: iterable}, return a set of all iterables

    >>> bunch({'a': {4, 5, 6}, 'b': set((1, 4, 7))})
    frozenset({1, 4, 5, 6, 7})
    """
    ret = set()
    for s in dic.values():
        if not hasattr(s, "__iter__"):
            s = set((s,))
        ret |= set(s)
    return frozenset(ret)


def bunch(dic):
    """given a dict {k: iterable}, return a set of all iterables

    >>> bunch({'a': {4, 5, 6}, 'b': set((1, 4, 7))})
    frozenset({1, 4, 5, 6, 7})
    """
    return frozenset(chain.from_iterable(dic.values()))


def object_attributes(obj, mode, blacklist=None):
    """list object attributes of a given type"""
    if not blacklist:
        blacklist = ()
    attrs = defaultdict(set)
    for k, v in dir(obj):
        if k in blacklist:
            continue
        if k.startswith("__"):
            attrs["protected"].add(k)
        elif k.startswith("_"):
            attrs["private"].add(k)
        else:
            attrs["public"].add(k)
    # ------------------------------------------------------------------------
    if mode in attrs:
        # public, private, protected
        return sorted(list(attrs[mode]))
    if mode == "both":
        return sorted(list(attrs["public"] | attrs["private"]))
    if mode == "all":
        return sorted(list(attrs["public"] | attrs["private"] | attrs["protected"]))
    raise KeyError(
        f'mode {mode} shall be one of {"public", "private", "protected", "both", "all"}'
    )


def check_path(filename, name="file") -> None:
    """checks that the file exists"""
    try:
        exists = os.path.exists(filename)
    except TypeError:
        msg = "cannot find %s=%r\n" % (name, filename)
        raise TypeError(msg)
    if not exists:
        msg = "cannot find %s=%r\n%s" % (name, filename)
        raise FileNotFoundError(msg)


def transform_dict_of_list(data):
    """transform a dict of list into a list of dict:

    >>> data = {'MIDi': [1002, 1003, 1009],
    ... 'SOUTi': ['NO', 'YES', 'YES'],
    ... 'Ti': [0.018, 0.339, 0.018],
    ... 'THETAi': [0.0, 0.0, 5.0]}
    >>> expected = [{'MIDi': 1002, 'SOUTi': 'NO', 'Ti': 0.018, 'THETAi': 0.0},
    ...             {'MIDi': 1003, 'SOUTi': 'YES', 'Ti': 0.339, 'THETAi': 0.0},
    ...             {'MIDi': 1009, 'SOUTi': 'YES', 'Ti': 0.018, 'THETAi': 5.0}]
    >>> transform_dict_of_list(data) == expected
    True
    """
    ret = []
    nb_items = len(data[next(iter(data.keys()))])
    for item_no in range(nb_items):
        _d = {}
        for fieldname, seq in data.items():
            _d[fieldname] = list(seq)[item_no]
        ret.append(_d)
    return ret


def chained_dot(obj, txt):
    subobjs = txt.split(".")
    subobj = obj
    for child in txt.split("."):
        subobj = getattr(subobj, child)
    return subobj


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
