"""
NastraIO decorators
"""

import inspect
import logging
import re
import time
import warnings
from collections import defaultdict
from functools import lru_cache, partial, wraps
from itertools import chain
from threading import RLock

import numpy as np
import pandas as pd

try:
    from pyinstrument import Profiler

    IS_PYINSTRUMENT = True
except ImportError:
    IS_PYINSTRUMENT = False

from numtools.vgextended import loc_array

from nastranio.constants import (
    AXIS,
    BOUNDARY,
    CARDS_REGISTER,
    ELEMENT,
    LOADING,
    MATERIAL,
    PROPERTY,
    UNKNOWN,
    GMSHElementTypes,
    VTKShapes,
)

_NOT_FOUND = object()


CACHES = defaultdict(list)


# from nastranio.constants import ELEMENT, MATERIAL, AXIS, UNKNOWN, LOADING, PROPERTY, BOUNDARIES
class cached_property:
    """backported from python3.8; modify cached name attribute from "<name>" to
    "{CACHED_PREFIX}{name}" to easily clear cache from the class itself
    """

    CACHED_PREFIX = "_cached_"

    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.lock = RLock()

    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = f"{self.CACHED_PREFIX}{name}"
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it."
            )
        try:
            cache = instance.__dict__
        except (
            AttributeError
        ):  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
        return val


def timeit(method=None, loglevel="info"):
    if not method:
        return partial(timeit, loglevel=loglevel)

    @wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        delta = te - ts
        name = method.__name__
        msg = f'function or method "{name}" took: {delta:.2f} sec.'
        if not loglevel:
            print(msg)
        else:
            getattr(logging, loglevel)(msg)
        return result

    return timed


def profile(f):
    @wraps(f)
    def wrap(*args, **kw):
        if not IS_PYINSTRUMENT:
            return f(*args, **kw)
        profiler = Profiler()
        profiler.start()
        result = f(*args, **kw)
        profiler.stop()
        name = f.__name__
        print(80 * "=")
        print('Profiling "%s"' % name)
        print(profiler.output_text(unicode=True, color=True))
        print(80 * "=")
        return result

    return wrap


def dump_args(decorated_function):
    """
    Function decorator logging entry + exit and parameters of functions.

    Entry and exit as logging.info, parameters as logging.DEBUG.
    """

    @wraps(decorated_function)
    def wrapper(*dec_fn_args, **dec_fn_kwargs):
        # Log function entry
        func_name = decorated_function.__name__
        log = logging.getLogger(func_name)
        log.debug("Entering {}()...".format(func_name))

        # get function params (args and kwargs)
        argnames = decorated_function.__code__.co_varnames
        if "self" in argnames:
            ix = argnames.index("self")
            clsname = dec_fn_args[ix].__class__.__name__
            log.info("method of %s" % clsname)

        args = {
            k: v for k, v in dict(zip(argnames, dec_fn_args)).items() if k != "self"
        }
        params = dict(args=args, kwargs=dec_fn_kwargs)

        log.info(
            "\t"
            + ", ".join(["{}={}".format(str(k), repr(v)) for k, v in params.items()])
        )
        # Execute wrapped (decorated) function:
        out = decorated_function(*dec_fn_args, **dec_fn_kwargs)
        log.debug("Done running {}()!".format(func_name))

        return out

    return wrapper


# Cards class decorators
# It difines at least (e.g.) unknown:
#    * cls.type
# ========================================================================
def unknown(cls):
    setattr(cls, "type", UNKNOWN)
    return cls


# ------------------------------------------------------------------------
# elements


def nb_nodes(self):
    return len(self.gids_header)


def cells(self, nasgids=None):
    """
    return element's cell definition.
    """
    gidnames = self.gids_header[:]  # ['G1', 'G2', 'G3']
    cells = []
    eids = self.carddata["main"][self.EID_FIELDNAME]
    # ========================================================================
    # default nasgids and naseids
    # ========================================================================
    if nasgids is None:
        nasgids = list(self._eid2gids.values())
        nasgids = np.array(sorted(list(chain(*nasgids))))
        logging.warning("no gids nor eids passed as reference")

    # append number of nodes
    cells.append(np.array(len(self) * [self.nb_nodes()]))
    gidnames.insert(0, "nbpoints")
    # ------------------------------------------------------------------------
    # map VTK nodes to NASTRAN nodes
    for gname in gidnames:
        if gname == "nbpoints":
            continue
        gids = self.carddata["main"][gname]
        gix = loc_array(nasgids, gids)
        cells.append(gix)

    payload = {"data": np.array(cells).T, "index": np.array(eids), "columns": gidnames}
    return payload


def to_vtk(self, nasgids, debug=True):
    """return data to build VTU unstructured file"""
    payload = self.cells(nasgids=nasgids)
    # len(payload['index'])== len(self) for most of the cards
    # except RBEs
    cell_types = len(payload["index"]) * [VTKShapes[self.shape]]
    cells = payload["data"].reshape(-1)
    eids = payload["index"].tolist()
    # offset = np.array([0, 5, ...])
    offset = np.arange(0, len(cells), self.nb_nodes() + 1)
    return {
        "cell_types": cell_types,
        "cells": cells,
        "eids": eids,
        "card": len(cell_types) * [self.card],
        "offset": offset,
    }


def eid2gids(self, keep_order=False, asdf=False):
    """return a dictionnary {'eid' <int>: 'gids': <set>} based on MAIN CARD data

    Also eventually call a `eid2gids_complement()` hook for cards having additional data
    to provide (eg. RBE2/RBE3).
    """
    if keep_order or asdf is True:
        eid2gids = self._eid2gids_ordered
    else:
        eid2gids = self._eid2gids
    if asdf:
        df = pd.DataFrame(eid2gids).T
        df.index.names = ["EID"]
        df.columns = self.gids_header
        return df

    return dict(eid2gids)


def update_gid(self, eid, gidno, new_gid):
    data = self.carddata["main"]
    eid_ix = data["EID"].index(eid)
    header = self.gids_header[gidno]  # -> eg. "GB"
    old_gid = data[header][eid_ix]
    data[header][eid_ix] = new_gid
    return eid_ix, old_gid


def element(dim, shape):
    def decorator(cls):
        CARDS_REGISTER.append(cls.__name__)
        setattr(cls, "type", ELEMENT)
        setattr(cls, "dim", dim)
        setattr(cls, "shape", shape)
        setattr(cls, "gmsh_eltype", GMSHElementTypes.get(shape))
        if not hasattr(cls, "eid2gids"):
            setattr(cls, "eid2gids", eid2gids)
        if not hasattr(cls, "cells"):
            setattr(cls, "cells", cells)
        if not hasattr(cls, "nb_nodes"):
            setattr(cls, "nb_nodes", nb_nodes)
        if not hasattr(cls, "update_gid"):
            setattr(cls, "update_gid", update_gid)
        if not hasattr(cls, "to_vtk"):
            setattr(cls, "to_vtk", to_vtk)
        if not hasattr(cls, "GIDS_PATTERN"):
            setattr(cls, "GIDS_PATTERN", re.compile(r"^G\d+$"))
        if not hasattr(cls, "THK_PATTERN"):
            setattr(cls, "THK_PATTERN", re.compile(r"^T\d+$"))
        if not hasattr(cls, "EID_FIELDNAME"):
            setattr(cls, "EID_FIELDNAME", "EID")
        if not hasattr(cls, "PID_FIELDNAME") and "PID" in cls.TABLE:
            setattr(cls, "PID_FIELDNAME", "PID")
        if not hasattr(cls, "XID_FIELDNAME"):
            setattr(cls, "XID_FIELDNAME", getattr(cls, "EID_FIELDNAME"))
        return cls

    return decorator


def fem_property(cls):
    CARDS_REGISTER.append(cls.__name__)
    setattr(cls, "type", PROPERTY)
    if not hasattr(cls, "PID_FIELDNAME") and "PID" in cls.TABLE:
        setattr(cls, "PID_FIELDNAME", "PID")
    if not hasattr(cls, "MATS_PATTERN"):
        setattr(cls, "MATS_PATTERN", re.compile(r"^MID\d*$"))
    if not hasattr(cls, "XID_FIELDNAME"):
        setattr(cls, "XID_FIELDNAME", getattr(cls, "PID_FIELDNAME"))
    return cls


def axis(cls):
    CARDS_REGISTER.append(cls.__name__)
    setattr(cls, "type", AXIS)
    return cls


def loading_type(typ=None):
    def decorator(cls):
        CARDS_REGISTER.append(cls.__name__)
        setattr(cls, "type", LOADING)
        if not hasattr(cls, "XID_FIELDNAME"):
            setattr(cls, "XID_FIELDNAME", "SID")
        if typ:
            if typ == "nodal":
                setattr(cls, "LOADING_TYPE", "nodes")
            elif typ == "elemental":
                setattr(cls, "LOADING_TYPE", "elements")
            else:
                raise ValueError(f"decorator 'loading_type' does not handle {typ=}")
        else:
            setattr(cls, "LOADING_TYPE", None)
        return cls

    return decorator


def boundary(cls):
    CARDS_REGISTER.append(cls.__name__)
    setattr(cls, "type", BOUNDARY)
    if not hasattr(cls, "XID_FIELDNAME"):
        setattr(cls, "XID_FIELDNAME", "SID")
    return cls


def material(cls):
    CARDS_REGISTER.append(cls.__name__)
    setattr(cls, "type", MATERIAL)
    if not hasattr(cls, "MID_FIELDNAME"):
        setattr(cls, "MID_FIELDNAME", "MID")
    if not hasattr(cls, "XID_FIELDNAME"):
        setattr(cls, "XID_FIELDNAME", getattr(cls, "MID_FIELDNAME"))
    return cls
