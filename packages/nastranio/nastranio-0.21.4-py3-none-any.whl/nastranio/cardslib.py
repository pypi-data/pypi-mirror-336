import json
import logging
import pickle
import re
import warnings
from base64 import b64decode, b64encode
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache

import numpy as np
import pandas as pd
from numpy.lib import recfunctions as rfn
from numtools.misc import replace_nan
from numtools.serializer import Serializer

from nastranio.constants import ELEMENT, PROPERTY, UNKNOWN
from nastranio.decorators import cached_property
from nastranio.fields_writer import (
    DefaultDict,
    fields_to_card,
    get_field,
    nbrows_by_fields,
    trans,
)
from nastranio.pylib import autoconvert
from nastranio.utils import array2dic, calcdiff, dic2array, transform_dict_of_list

try:
    import msgpack

    ISMSGPACK = True
except ImportError:
    ISMSGPACK = False

pat = re.compile(r"(?P<root>\w+)(?P<id>\d+)")

# ============================================================================
# json encoder / decoder
# ============================================================================


class PythonObjectEncoder(json.JSONEncoder):
    """encode sets to json"""

    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {"_python_object": b64encode(pickle.dumps(obj)).decode("utf-8")}


def as_python_object(dct):
    if "_python_object" in dct:
        return pickle.loads(b64decode(dct["_python_object"].encode("utf-8")))
    return dct


# ============================================================================
# msgpack encoder / decoder
# ============================================================================


def msgpack_encode(obj):
    if isinstance(obj, set):
        obj = {"__set__": True, "as_list": list(obj)}
    return obj


def msgpack_decode(obj):
    if "__set__" in obj:
        obj = set(obj["as_list"])
    return obj


# ============================================================================
# parsing helpers
# ============================================================================


def parse_table(table, asruler=False, linesno=None):
    r"""parse a Nastran user-guide style table,
    and return a tuple (`card`, `fields`, `repeated`)

    >>> table = (
    ...    '| 1    | 2   | 3   | 4   | 5  | 6  | 7  | 8   | 9  | 10 |\n'
    ...    '|------+-----+-----+-----+----+----+----+-----+----+----|\n'
    ...    '| PBAR | PID | MID | A   | I1 | I2 | J  | NSM |    |\n'
    ...    '| ""   | K1  | K2  | I12 |    |    |    |     |    |\n')
    >>> card, fields, repeated = parse_table(table)
    >>> card
    'PBAR'
    >>> fields
    {2: 'PID', 3: 'MID', 4: 'A', 5: 'I1', 6: 'I2', 7: 'J', 8: 'NSM', 12: 'K1', 13: 'K2', 14: 'I12'}
    >>> repeated  # -> None

    It also handles tables using -etc.- fields:

    >>> table = (
    ...    '| 1     | 2    | 3  | 4      | 5     | 6      | 7    | 8      | 9     | 10 |\n'
    ...    '|-------+------+----+--------+-------+--------+------+--------+-------+----|\n'
    ...    '| PCOMP | PID  | Z0 | NSM    | SB    | FT     | TREF | GE     | LAM   | \n'
    ...    '| ""    | MID1 | T1 | THETA1 | SOUT1 | MID2   | T2   | THETA2 | SOUT2 | \n'
    ...    '| ""    | MID3 | T3 | THETA3 | SOUT3 | -etc.- |      |        |       | \n')
    >>> card, fields, repeated = parse_table(table)
    >>> card
    'PCOMP'
    >>> fields
    {2: 'PID', 3: 'Z0', 4: 'NSM', 5: 'SB', 6: 'FT', 7: 'TREF', 8: 'GE', 9: 'LAM'}
    >>> repeated
    {'starts@': 12, 'fields': ['MID', 'T', 'THETA', 'SOUT']}

     -etc.- is not supposed to be trailing:

    >>> table = (
    ...    '| 1    | 2    | 3   | 4   | 5      | 6      | 7   | 8   | 9   | 10 |\n'
    ...    '|------+------+-----+-----+--------+--------+-----+-----+-----+----|\n'
    ...    '| RBE2 | EID  | GN  | CM  | GM1    | GM2    | GM3 | GM4 | GM5 |    | \n'
    ...    '| ""   | GM6  | GM7 | GM8 | -etc.- | ALPHA  |     |     |     |    | \n')
    >>> card, fields, repeated = parse_table(table)
    >>> card
    'RBE2'
    >>> fields
    {2: 'EID', 3: 'GN', 4: 'CM'}
    >>> repeated
    {'starts@': 5, 'fields': ['GM'], 'floating': ['ALPHA']}
    """
    lines = [l.strip() for l in table.split("\n")]
    lines = [l for l in lines if l]
    # ---------------------------------------
    # ensure first line is field numbering
    if set(lines[0]) == {" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "|"}:
        lines = lines[1:]
    # ---------------------------------------
    # check if second line is grid decoration
    if set(lines[0]) == {"+", "-", "|"}:
        lines = lines[1:]
    if linesno:
        lines = [l for i, l in enumerate(lines) if i in linesno]
    # ---------------------------------------
    # get fields
    fields = {}
    for i, line in enumerate(lines):
        _fields = line.split("|")
        # since grid has trailing and heading "|" characters, we need to remove first and last fields
        _fields = [f.strip() for f in _fields[1:-1]]
        fields.update(dict(zip(range(1 + i * 10, len(_fields) + 1 + i * 10), _fields)))
    # ---------------------------------------
    # clean fields: remove empty fields
    for k, v in fields.copy().items():
        if v.strip() in ("", '""'):
            fields.pop(k)
    if asruler:
        # --------------------------------------------------------------------
        # ensure all fields length < 8 characters
        for k, fieldname in fields.items():
            if len(fieldname) > 6:
                fields[k] = fieldname[:5] + ".."
        repeated = {}
    elif "-etc.-" in fields.values():
        etc_key = {v: k for k, v in fields.items()}["-etc.-"]
        floating = list({k: v for k, v in fields.items() if k > etc_key}.values())
        fields = {k: v for k, v in fields.items() if k < etc_key}
        # repeated fields can be one or more.
        # iterate from last field until we find a repeted pattern
        i = -1
        keys = list(fields.keys())
        repeated = {"starts@": None, "fields": []}
        while True:
            key = keys[i]
            value = fields[key]
            field, nb = pat.search(value).groups()
            if field in repeated["fields"]:
                break
            repeated["fields"].append(field)
            i -= 1
        repeated["fields"] = repeated["fields"][::-1]
        # clean all the repeated fields
        for key in keys[::-1]:
            value = fields[key]
            try:
                field, nb = pat.search(value).groups()
            except:
                break
            else:
                fields.pop(key)
                repeated["starts@"] = key
        if floating:
            repeated["floating"] = floating
    else:
        repeated = None
    if 1 in fields:
        card = fields.pop(1)
    else:
        card = None
    return card, fields, repeated


class DummyFields:
    """drop-in replacement for fields dict. Used by anonymous cards"""

    def __getitem__(self, x):
        return "FIELD#%d" % x


# ============================================================================
# Cards Skeletons to be derived
# ============================================================================


class SimpleCard(Serializer):
    """defines generically simple cards (eg. GRID, CQUAD4),
    or cycling cards (eg. PCOMP)
    """

    TABLE = None
    DEFAULTS = {}
    MULT_TYPES_FIELDS = {}
    type = UNKNOWN

    def __init__(self, name=None, data=None):
        if not name:
            name = self.__class__.__name__
        self.name = name
        if hasattr(self, "TABLE") and self.TABLE is not None:
            self.card, self.fields, self.repeated = parse_table(self.TABLE)
        else:
            self.card = name
            self.fields = {}  # DummyFields()
            self.repeated = None
        # --------------------------------------------------------------------
        # main property (existing for all cards)
        self.carddata = {"main": defaultdict(list)}
        if data:
            self.resume(data)
        # if _is_dummy:
        #     # build fields based on field number
        #     _fields = dict(self.carddata["main"])
        #     fields = dict(zip(range(0, len(_fields)), _fields.keys()))
        #     self.fields = {
        #         k: v for k, v in fields.items() if (k % 10 != 0 and (k - 1) % 10 != 0)
        #     }

    @classmethod
    def fields_info(cls):
        _data = parse_table(cls.TABLE)
        all_fields = tuple(_data[1].values())
        repeated = _data[2]
        fields = {
            # mandatory needs to keep order
            "mandatory": tuple([f for f in all_fields if f not in cls.DEFAULTS]),
            "optional": set([f for f in all_fields if f in cls.DEFAULTS]),
        }
        if repeated:
            fields["repeated"] = tuple([f"{field}i" for field in repeated["fields"]])
        return fields

    @cached_property
    def _rowno2id(self):
        """map carddata row number to card IDs"""
        return {i: id for i, id in enumerate(self.carddata["main"][self.XID_FIELDNAME])}

    @cached_property
    def _id2rowno(self):
        """map card IDs to carddata row number"""
        return {id: i for i, id in enumerate(self.carddata["main"][self.XID_FIELDNAME])}

    def _list_caches(self):
        return {k for k in self.__dict__ if k.startswith(cached_property.CACHED_PREFIX)}

    def clear_caches(self, rebuild=True):
        """delete internal caches"""
        prefix = cached_property.CACHED_PREFIX
        cache_names = self._list_caches()  # _cache_XXX
        cached_names = [k.replace(prefix, "") for k in cache_names]  # XXX
        logging.info("clean cached properties: %s", ", ".join(cached_names))
        _rebuilt = []
        for fcached, cache_name in zip(cached_names, cache_names):
            self.__dict__.pop(cache_name)
            if rebuild:
                # fcached = cached_name.replace(prefix, "")
                getattr(self, fcached)
                _rebuilt.append(fcached)
        if _rebuilt:
            logging.info("rebuilt cache: %s", ", ".join(_rebuilt))

    def default_to_nan(self, transfields=True):
        def _default_to_nan(row):
            """change default values to None"""
            for k, v in row.items():
                v = self._check_default(k, v, None)
                if transfields:
                    v = trans(v)
                row[k] = v
            return row

        df = pd.DataFrame(self.array)
        df = df.astype(object).apply(_default_to_nan, axis=1)
        if transfields:
            df = df.fillna("")
        return df

    def diff(self, other):
        return calcdiff((self.__dict__, other.__dict__))

    def __eq__(self, other):
        return len(self.diff(other)) == 0

    def _reset(self):
        name = self.name
        self.__dict__ = {}
        self.__init__(name=name)

    # def __getattr__(self, attr):
    #     """bind carddata contents"""
    #     if attr in self.carddata:
    #         return self.carddata[attr]
    #     raise AttributeError(attr)

    def __len__(self):
        keys = list(self.carddata["main"].keys())
        if len(keys) == 0:
            return 0
        key = keys[0]
        return len(self.carddata["main"][key])

    def help(self, doprint=False):
        """
        return self.TABLE usable as ruler
        """
        card, fields, repeated = parse_table(self.TABLE, asruler=True)
        # substitute fields keys with appropriate placeholder
        ruler_fieldsmap = DefaultDict(fn1=card)
        ruler_fieldsmap.update({"fn%d" % k: field for k, field in fields.items()})
        lines = fields_to_card(ruler_fieldsmap, leading="$", sep="▕")
        if not doprint:
            return lines
        print("\n".join(lines))

    def _check_default(self, key, value, default=None):
        if default is None:
            default = self.DEFAULTS
        if key in default and value == default[key]:
            value = None
        return value

    def _to_nastran(self, ids=frozenset(), ruler=False, additional_ruler_lines=()):
        """
        common code for all `to_nastran` functions
        """
        # create a DefaultDict dict mapping placeholders "fnXX" to field names
        # {'fn1': 'CORD2R', 'fn2': 'CID', ..., 'fn12': 'C1', 'fn13': 'C2', 'fn14': 'C3', }
        fieldsmap = DefaultDict(fn1=self.card)  # , fn10='+', fn11='+')
        try:
            fieldsmap.update({"fn%d" % k: v for k, v in self.fields.items()})
        except:
            print(self.fields)
            raise
        lines = []
        # creating a ruler is as simple as:
        if ruler:
            lines += self.help()
            if additional_ruler_lines:
                lines += additional_ruler_lines
        # ---------------------------------------------------------------
        # associate carddata['main'] entries to fields
        field = self.fields[2]
        all_ids = self.carddata["main"][field]  # eg. [eid1, eid2, ...]
        ids = set(ids) & set(all_ids)
        if not ids:
            ids = set(all_ids)
        # associate card number in the list to card ID
        full_array = self.array
        _isin = np.isin(full_array[field], list(ids))
        array = full_array[_isin]
        ixs = np.flatnonzero(_isin)
        return fieldsmap, lines, zip(ixs, array[field])

    def _newline(self, fieldsmap, ix, with_default):
        # build a new row
        data = DefaultDict(fn1=self.card)
        for fieldcode, fieldname in fieldsmap.items():
            if fieldcode in ("fn1",) or fieldname in ("+"):
                continue
            value = replace_nan(self.carddata["main"][fieldname][ix])
            if not with_default:
                value = self._check_default(fieldname, value, default=self.DEFAULTS)
            data[fieldcode] = trans(value)
        return data

    def to_nastran(
        self, ids=frozenset(), ruler=False, with_default=True, comments=None
    ):
        """
        Convert a collection of cards to 8-chars NASTRAN format.
        SimpleCard to_nastran()"""
        fieldsmap, lines, ixid = self._to_nastran(ids=ids, ruler=ruler)
        for ix, id in ixid:
            # initiate a new line and populate a data dict with fixed fields
            try:
                data = self._newline(fieldsmap, ix, with_default)
            except ValueError as exc:
                logging.critical(f"cannot make new line for {self.name} {ix}")
                raise
            if comments and hasattr(self, "COMMENTS_KEY"):
                comment = comments.get(self.COMMENTS_KEY, dict()).get(id, dict())
                if comment:
                    lines.append(f"$ Femap {self.COMMENTS_KEY} {id} : {comment}")
            lines += fields_to_card(data)
        return lines

    def merge(self, other):
        """attempt to create a universal merge() method working for
        SimpleCard, SimpleCyclingCard and ComplexCard
        """
        # --------------------------------------------------------------------
        # merge all fields but the extended data IDs
        assert self.name == other.name
        # count for later checks
        nb_ini = len(self)
        nb_to_add = len(other)
        for k, v in other.carddata["main"].items():
            # avoid reference fields
            dataname, *_ = k.split("ID")
            if dataname in self.carddata:
                continue
            self.carddata["main"][k] += v
        # --------------------------------------------------------------------
        # merge extended data
        for dataname in self.carddata.keys():
            if dataname == "main":
                continue
            colname = "%sID" % dataname
            offset = max(self.carddata["main"][colname]) + 1
            other._offset_repeated_ix(colname, offset=offset)
            sd = self.carddata[dataname]
            od = other.carddata[dataname]
            sd += od
            self.carddata["main"][colname] += other.carddata["main"][colname]
        # --------------------------------------------------------------------
        # deduplicate
        self.dedup()

    def dedup(self):
        """
        parse additional data to find and remove duplicates
        """
        for dataname in self.carddata.keys():
            if dataname == "main":
                continue
            colname = "%sID" % dataname
            data = self.carddata[dataname]
            dedup_data = []  # this will override self.carddata[dataname]
            for ix, dataset in enumerate(data):
                if dataset not in dedup_data:
                    dedup_data.append(dataset)
                    continue
                # dataset is duplicated; change referencing ID
                already_ix = dedup_data.index(dataset)
                self.carddata["main"][colname][ix] = already_ix
            self.carddata[dataname] = dedup_data

    def _offset_repeated_ix(self, colname, offset):
        """offset indices of repeated data in both `main` and
        `self.REPEATED_DATA_NAME`
        """
        old = self.carddata["main"][colname]
        new = [(ix + offset) for ix in old]
        old2new = dict(zip(old, new))
        self.carddata["main"][colname] = [
            old2new[ix] for ix in self.carddata["main"][colname]
        ]

    def append_sparams(self, sparams, **kwargs):
        """fields are provided as `sparams` dictionnary header: value"""
        _sparams = self.DEFAULTS.copy()
        _sparams.update(sparams)
        # reorder fields
        _sparams = {k: _sparams[k] for k in self.fields.values()}
        # if hasattr(self, "clean_sparams"):
        #     self.clean_params(_sparams)
        for header, value in _sparams.items():
            if value is None:
                value = self.DEFAULTS.get(header, value)
            self.carddata["main"][header].append(value)
            # route multiple types fields
            if header in self.MULT_TYPES_FIELDS:
                alternatives = self.MULT_TYPES_FIELDS[header].copy()
                try:
                    # a value (other than None) has been found
                    # we can therefore guess the field name
                    routed_header = alternatives.pop(type(value))
                    self.carddata["main"][routed_header].append(value)
                except KeyError:
                    pass
                # only remains the alternate field
                for typ, routed_header in alternatives.items():
                    self.carddata["main"][routed_header].append(None)
        # =====================================================================
        # repeated fields
        # LOAD: {'starts@': 4, 'fields': ['S', 'L']}
        # PCOMP: {'starts@': 12, 'fields': ['MID', 'T', 'THETA', 'SOUT']}
        # RBE2: {'starts@': 5, 'fields': ['GM'], 'floating': ['ALPHA']}
        # RBE3: {'starts@': 33, 'fields': ['GM', 'CM'], 'floating': ['"ALPHA"', 'ALPHA']}
        # SPC1: {'starts@': 4, 'fields': ['G']}
        # =====================================================================
        if not kwargs:
            return
        repeated_fields_specs = set(self.fields_info()["repeated"])
        # ---------------------------------------------------------------------
        # ensure we do not have floating repetitions
        # for now, only simple single-field repetitions are handled
        if "floating" in repeated_fields_specs:
            raise NotImplementedError("do not handle for now floating repetitions")
        # ---------------------------------------------------------------------
        # repeated MUST finish with 'i'.
        # TODO: discard this test?
        for repeated_input in kwargs:
            if not repeated_input.endswith("i"):
                raise ValueError(f"repeated field {repeated_input} not understood")
        # ---------------------------------------------------------------------
        # get rid of training "i"
        data = {k[:-1]: v for k, v in kwargs.items()}  # 'Gi' -> 'G'
        # and transform a dict of list into a list of dict
        data = transform_dict_of_list(data)
        # ---------------------------------------------------------------------
        # append data
        self.carddata["main"][self.REPEATED_DATA_NAME + "ID"].append(
            self.nb_items() - 1
        )
        self.carddata[self.REPEATED_DATA_NAME].append(data)

    def nb_items(self):
        try:
            return len(self.carddata["main"][next(iter(self.carddata["main"].keys()))])
        except StopIteration:
            return 0

    def append_fields_list(self, fields):
        """fields are provided as text, without the card name"""
        # insert TWO dummy fields such as index in fields list match NASTRAN field
        fields = ["_", "_"] + fields
        # ==================================================================
        # read fixed fields
        # ==================================================================
        if not hasattr(self.fields, "items"):
            raise AttributeError("card %s has no fields items" % self)
        kwargs = {}
        for ix, header in self.fields.items():
            try:
                value = fields[ix]
            except IndexError:
                value = None
            kwargs[header] = value
        self.append_sparams(kwargs)
        return fields

    def append_legacy(self, fields):
        """fields are provided as text, without the card name"""
        # insert TWO dummy fields such as index in fields list match NASTRAN field
        fields = ["_", "_"] + fields
        # ==================================================================
        # read fixed fields
        # ==================================================================
        if not hasattr(self.fields, "items"):
            raise AttributeError("card %s has no fields items" % self)
        for ix, header in self.fields.items():
            try:
                value = fields[ix]
            except IndexError:
                value = None
            if value is None:
                value = self.DEFAULTS.get(header, value)
            self.carddata["main"][header].append(value)
            # route multiple types fields
            if header in self.MULT_TYPES_FIELDS:
                alternatives = self.MULT_TYPES_FIELDS[header].copy()
                routed_header = alternatives.pop(type(value))
                self.carddata["main"][routed_header].append(value)
                # only remains the alternate field
                for typ, routed_header in alternatives.items():
                    self.carddata["main"][routed_header].append(None)
        return fields

    def parse(self, txt, debug=False):
        """simple parser for NASTRAN small-fields bulk entry.

        ⚠ Only to be used for testing purposes! ⚠
        """
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        if debug:
            import pprint

            pprint.pprint(lines)  # TODO: remove me!
        fields = []
        for l in lines:
            if l.startswith("$"):
                continue
            for fieldID in range(10):
                sub = slice(fieldID * 8, fieldID * 8 + 8)
                fields.append(autoconvert(l[sub].strip()))
        # trim None
        while fields[-1] is None:
            fields.pop(-1)
        if debug:
            print("fields:\n", fields)
        self.append_fields_list(fields[1:])

    def export_data(self):
        """export_data data for serialization"""
        res = deepcopy(self.carddata)
        res["main"] = dict(res["main"])  # defaultdict -> dict
        res["card"] = self.name
        return res

    def resume(self, data):
        """resume card from data,
        such as PCOMP = PCOMP.resume(PCOMP.export_data()) == PCOMP
        """
        self._reset()
        # data = deepcopy(data)
        cardname = data.pop("card")
        if cardname != self.card:
            raise ValueError(
                f'provided cardname "{cardname}" differes from %s' % self.card
            )
        assert cardname == self.card
        for ksrc, ktarget in data.items():
            # keep defaultdict for 'main' data
            if ksrc in self.carddata and hasattr(data[ksrc], "update"):
                self.carddata[ksrc].update(data[ksrc])
            else:
                self.carddata[ksrc] = data[ksrc]

    def __getstate__(self):
        return self.__dict__
        # return {k : v for k, v in self.__dict__.items() if not k.startswith('_cached_')}

    @property
    def array(self):
        """return carddata['main'] as numpy structured arrays"""
        return dic2array(self.carddata["main"])

    def ids(self):
        return set(self.carddata["main"][self.XID_FIELDNAME])

    def query_id(self, value, asview=False, with_loc=False):
        """
        return a tuple (arr, rownbs)
        """
        if isinstance(value, int):
            loc = np.where(self.array[self.XID_FIELDNAME] == value)
            value = self.array[loc]
        else:
            # assume a list has been passed
            mask = np.isin(self.array[self.XID_FIELDNAME], list(value))
            value = self.array[np.where(mask)]
            if with_loc:
                loc = [i for i, v in enumerate(mask) if v]
        if asview:
            value = value.view(asview)
        if with_loc:
            return value, loc
        return value

    def query_id_fast(self, value, columns=None, asview=False):
        """
        fast version of query_id
        return a tuple (arr, rownbs)
        """

        ids = self.carddata["main"][self.XID_FIELDNAME]
        loc = self.query_loc(value)
        if not columns:
            subset = {k: [v[i] for i in loc] for k, v in self.carddata["main"].items()}
        else:
            subset = {k: [self.carddata["main"][k][i] for i in loc] for k in columns}
        if asview:
            subset = np.array(list(subset.values())).T
            if len(loc) == 1:
                return subset[0]
        elif len(loc) == 1:
            subset = {k: v[0] for k, v in subset.items()}
        return subset

    def query_loc(self, value):
        """
        return location in carddata lists
        """
        ids = self.carddata["main"][self.XID_FIELDNAME]
        if isinstance(value, int):
            return [ids.index(value)]
        # assume a list has been passed
        return [ids.index(v) for v in value]

    def _extract_array(self, index, columns, values_type="float64", index_type="int"):
        """transform a numpy structured array into {'data': values, 'index': index, 'columns': columns}"""
        sarr = self.array
        values = rfn.structured_to_unstructured(sarr[columns], dtype=values_type)
        index = rfn.structured_to_unstructured(
            sarr[[index]], dtype=index_type
        ).flatten()
        return {"data": values, "index": index, "columns": columns}

    def subset(self, eids=None):
        """return a card object with selected subset"""
        if self.type != ELEMENT:
            raise AttributeError("gids_header")
        array = self.array
        if eids is None:
            eids = array[self.EID_FIELDNAME].tolist()
        # --------------------------------------------------------------------
        # convert eids to numpy indices
        ixs = np.where(
            np.isin(np.array(self.carddata["main"][self.EID_FIELDNAME]), eids)
        )[0]
        _array = array[ixs]
        newdata = {"main": array2dic(_array, astype=list), "card": self.name}
        for k, vs in self.carddata.items():
            if k == "main":
                continue
            # ----------------------------------------------------------------
            # restrict additional data to relevant eids
            ix = newdata["main"][f"{k}ID"]
            vs = [vs[i] for i in ix]
            newdata[k] = vs
            newdata["main"][f"{k}ID"] = list(range(len(ix)))
        obj = self.__class__(data=newdata)
        return obj

    # ========================================================================
    # cachable attributes previously set by decorators
    # ========================================================================
    @cached_property
    def thk(self):
        """return a dict {eid: thk}"""
        if self.type != ELEMENT or self.dim != "2d" or self.THK_PATTERN is None:
            raise AttributeError("thk")
        # get thicknesses columns
        gids_cols = [
            col for col in self.carddata["main"] if self.THK_PATTERN.match(col)
        ]
        _data = self._extract_array("EID", gids_cols)
        _data["data"] = _data["data"].mean(axis=1)
        _data["name"] = "thk"
        _data.pop("columns")
        return _data

    @cached_property
    def gids_header(self):
        """return a list of Grid IDs headers (eg. ['G1', 'G3', 'G3'])"""
        return self._gids_header()

    @classmethod
    @lru_cache
    def _gids_header(cls):
        """return a list of Grid IDs headers (eg. ['G1', 'G3', 'G3'])"""
        if cls.type != "element":
            raise AttributeError("gids_header")
        gids_cols = [
            col for col in cls.fields_info()["mandatory"] if cls.GIDS_PATTERN.match(col)
        ]
        return gids_cols

    @cached_property
    def mids_header(self):
        """return a list of Grid IDs headers (eg. ['G1', 'G3', 'G3'])"""
        if self.type != PROPERTY:
            raise AttributeError("mids_header")
        mids_cols = [
            col for col in self.carddata["main"] if self.MATS_PATTERN.match(col)
        ]
        return mids_cols

    @cached_property
    def pid2mids(self):
        """return a mapping {PID: frozenset((MIDS))}

        this basic property is OK for basic properties like PROD, PSHELL, *etc.*
        but is not aware of PCOMP, for example. This needs therefore
        to be overriden in those later cases
        """
        if self.type != PROPERTY:
            raise AttributeError("pid2mids")
        ret = {}

        for ix, pid in enumerate(self.carddata["main"]["PID"]):
            ret[pid] = set()
            for midh in self.mids_header:
                mid = self.carddata["main"][midh][ix]
                # print(f'pid {pid}; midh {midh}:: {mid}')
                if mid:  # mid can be `None`; skip this case
                    ret[pid].add(mid)
            ret[pid] = frozenset(ret[pid])
        return ret

    @cached_property
    def _eid2gids_ordered(self):
        if self.type != ELEMENT:
            raise AttributeError("gids_header")
        gids_cols = self.gids_header
        eid2gids = defaultdict(set)
        for ix, eid in enumerate(self.carddata["main"][self.EID_FIELDNAME]):
            eid2gids[eid] = [self.carddata["main"][c][ix] for c in gids_cols]
            if hasattr(self, "eid2gids_complement"):
                # if list == set:
                #     eid2gids[eid] |= self.eid2gids_complement(eid=eid, ix=ix)
                # else:
                nb_meaningfull = len(self.gids_header)
                if nb_meaningfull == 1:
                    msg = f"Only the first ID is meaningfull"
                else:
                    msg = f"Only the first {nb_meaningfull} IDs are meaningfull"
                logging.info(msg)
                eid2gids[eid] += list(self.eid2gids_complement(eid=eid, ix=ix))
        return dict(eid2gids)

    @cached_property
    def _eid2gids(self):
        if self.type != ELEMENT:
            raise AttributeError("gids_header")
        gids_cols = self.gids_header
        eid2gids = defaultdict(set)
        for ix, eid in enumerate(self.carddata["main"][self.EID_FIELDNAME]):
            eid2gids[eid] = set(self.carddata["main"][c][ix] for c in gids_cols)
            if hasattr(self, "eid2gids_complement"):
                eid2gids[eid] |= self.eid2gids_complement(eid=eid, ix=ix)
        return dict(eid2gids)


class RepeatedRowsCard(SimpleCard):
    """Mother Card for cards dfining **ONE SINGLE** 'etc.'"""

    # ------------------------------------------------------------------------
    # tables
    TABLE = None
    REPEATED_ROWS_TABLE = None
    TRAILING_ROWS_TABLE = None
    # ------------------------------------------------------------------------
    # more stuff
    REPEATED_ROWS_NAME = None  # eg. 'stations' for PBEAM
    TRIGGER_REPEATED_ON = str
    SKIP_NEXT_ROW_ON = ()  # e.g. for PBEAM: ('SO', ('YESA', 'NO'))

    def __init__(self, name=None, data=None):
        super().__init__(name=name, data=data)
        self.REPEATED_ROWS_NAME = "{}_{}".format(
            self.name.lower(), self.REPEATED_ROWS_NAME.lower()
        )
        # assert self.repeated is not None
        # set-up an additional container for repeated rows
        self.carddata[self.REPEATED_ROWS_NAME] = []

    def append_fields_list(self, fields):
        fields = super().append_fields_list(fields)  # append regular fields
        # ==================================================================
        # read repeated rows
        # ==================================================================
        # card_subset:  one single PER card
        # example for PBEAM:
        #    {'SO': 'YES', 'X/XB': 0.3, etc...}
        card_subset = dict()
        # card_set: several (at least one) PER card
        # example for PCOMP:
        #   [{'SO': 'YES', 'X/XB': 0.3, etc...},
        #    {'SO': 'YES', 'X/XB': 0.7, etc...}]
        card_set = []
        # --------------------------------------------------------------------
        # analyse REPEATED_ROWS_TABLE and TRAILING_ROWS_TABLE
        _, repfields, _ = parse_table(self.REPEATED_ROWS_TABLE)
        _, trailfields, _ = parse_table(self.TRAILING_ROWS_TABLE)
        # ====================================================================
        # assuming that at least ONE block of repeated rows exists
        # this is True for PBEAM, see [ref.] remark #4
        # ====================================================================
        remaining_fields = fields[get_field(max(self.fields.keys()) + 1) :]
        remaining_fields = ["_", "_"] + remaining_fields
        # nbrepeated_rows = nbrows_by_fields(repfields)
        # offset = nbrepeated_rows * 10  # offset to apply each time we parse a block
        # --------------------------------------------------------------------
        # if some rows need to be skipped...
        _rev_repfields = {
            fieldname: fieldID for fieldID, fieldname in repfields.items()
        }
        try:
            _skipped_fieldID = _rev_repfields[self.SKIP_NEXT_ROW_ON[0]]
            _skipped_on = self.SKIP_NEXT_ROW_ON[1]
        except:
            _skipped_fieldID, _skip_on = None, None
            __import__("pdb").set_trace()
        while isinstance(remaining_fields[2], self.TRIGGER_REPEATED_ON):
            card_subset = dict()
            # number of rows to parse using repfields
            _skipped_field = remaining_fields[_skipped_fieldID]
            if _skipped_field in _skipped_on:  # if SO in ('YESA', 'NO'):
                block_length = 10
            else:
                block_length = 20
            block = remaining_fields[:block_length]
            remaining_fields = remaining_fields[block_length:]
            # build card_subset
            for ix, header in repfields.items():
                try:
                    card_subset[header] = block[ix]
                except IndexError:
                    card_subset[header] = None
            card_set.append(card_subset)
        card_set_ix = len(self.carddata[self.REPEATED_ROWS_NAME])
        self.carddata["main"][self.REPEATED_ROWS_NAME + "ID"].append(card_set_ix)
        self.carddata[self.REPEATED_ROWS_NAME].append(card_set)
        # ====================================================================
        # trailing fields are for the TRAILING_ROWS_TABLE
        # ====================================================================
        if remaining_fields:
            for ix, header in trailfields.items():
                try:
                    self.carddata["main"][header].append(remaining_fields[ix])
                except IndexError:
                    self.carddata["main"][header].append(None)
        return fields

    def to_nastran(
        self, ids=frozenset(), ruler=False, with_default=True, comments=None
    ):
        """
        Convert a collection of cards to 8-chars NASTRAN format.
        RepeatedRowsCard to_nastran()"""

        ffieldsmap, lines, ixid = self._to_nastran(
            ids=ids, ruler=ruler, additional_ruler_lines=["$ + repeated fields..."]
        )

        for ix, id in ixid:
            # initiate a new line and populate a data dict with fixed fields
            try:
                data = self._newline(ffieldsmap, ix, with_default)
            except ValueError as exc:
                logging.critical(f"cannot make new line for {self.name} {ix}")
                raise
            # ----------------------------------------------------------------
            # repeated rows
            _skipped_fieldname, _skipped_on = self.SKIP_NEXT_ROW_ON
            card_set = self.carddata[self.REPEATED_ROWS_NAME][ix]
            _offset = get_field(max([int(k[2:]) for k in data.keys()]) + 1) - 2
            for i, subset in enumerate(card_set):
                if (
                    subset[_skipped_fieldname] in _skipped_on
                ):  # if subset['SO'] in ('YESA', 'NO'):
                    _, repfields, _ = parse_table(self.REPEATED_ROWS_TABLE, linesno=[0])
                else:
                    _, repfields, _ = parse_table(self.REPEATED_ROWS_TABLE)
                offset = _offset + i * _offset
                fieldsmap = DefaultDict()  # , fn10='+', fn11='+')
                fieldsmap.update(
                    {"fn%d" % (k + offset): v for k, v in repfields.items()}
                )
                for fieldcode, fieldname in fieldsmap.items():
                    if fieldcode == "+":
                        continue
                    data[fieldcode] = trans(subset[fieldname])
            # ----------------------------------------------------------------
            # trailing rows

            _, trailfields, _ = parse_table(self.TRAILING_ROWS_TABLE)
            nextfield = get_field(max([int(k[2:]) for k in data.keys()]) + 1) - 2
            trailfields = {k + nextfield: v for k, v in trailfields.items()}
            for fieldcode, fieldname in trailfields.items():
                if fieldcode == "+":
                    continue
                data["fn%d" % fieldcode] = trans(self.carddata["main"][fieldname][ix])
            try:
                lines += fields_to_card(data)
            except:
                __import__("pdb").set_trace()
        return lines


class SimpleCyclingCard(SimpleCard):
    """Mother Card for cards dfining **ONE SINGLE** 'etc.'"""

    REPEATED_DATA_NAME = None  # eg. 'LAYUP'
    TABLE = None
    REPEATED_DEFAULTS = {}

    def __init__(self, name=None, data=None):
        super().__init__(name=name, data=data)
        if data is None:
            self.REPEATED_DATA_NAME = "{}_{}".format(
                self.name.lower(), self.REPEATED_DATA_NAME.lower()
            )
            # assert self.repeated is not None
            # set-up an additional container for cycling data
            self.carddata[self.REPEATED_DATA_NAME] = []

    def to_nastran(
        self, ids=frozenset(), ruler=False, with_default=True, comments=None
    ):
        """
        Convert a collection of cards to 8-chars NASTRAN format.
        SimpleCyclingCard to_nastran()"""

        fieldsmap, lines, ixid = self._to_nastran(ids=ids, ruler=ruler)
        for ix, id in ixid:
            # initiate a new line and populate a data dict with fixed fields
            try:
                data = self._newline(fieldsmap, ix, with_default)
            except ValueError as exc:
                logging.critical(
                    f"cannot make new line for {self.name} {ix} {id=} {fieldsmap=} {with_default=}"
                )
                breakpoint()
                raise
            # repeated data
            # self.carddata['main'][self.REPEATED_DATA_NAME + 'ID']
            rdata_id = self.carddata["main"][self.REPEATED_DATA_NAME + "ID"][ix]
            rdata = self.carddata[self.REPEATED_DATA_NAME][rdata_id]
            # reset field pointer
            field_pnt = self.repeated["starts@"]
            # iterate over repeated data for the current line
            for id, dataset in enumerate(rdata):
                for fieldname in self.repeated["fields"]:
                    field_pnt = get_field(field_pnt)
                    fieldcode = "fn%d" % field_pnt
                    value = dataset[fieldname]
                    if not with_default:
                        value = self._check_default(
                            fieldname, value, default=self.REPEATED_DEFAULTS
                        )
                    data[fieldcode] = trans(value)
                    field_pnt = field_pnt + 1
            # ----------------------------------------------------------------
            # floating (trailing) data
            floating_fields = self.repeated.get("floating", [])
            for fieldname in floating_fields:
                field_pnt = get_field(field_pnt)
                fieldcode = "fn%d" % field_pnt
                value = self.carddata["main"][fieldname][ix]
                if not with_default:
                    value = self._check_default(fieldname, value, default=self.DEFAULTS)
                data[fieldcode] = trans(value)
                field_pnt = field_pnt + 1
            lines += fields_to_card(data)
        return lines

    def append_fields_list(self, fields):
        fields = super().append_fields_list(fields)  # append regular fields
        # ==================================================================
        # read cycling fields, if any...
        # ==================================================================
        # card_subset:  one single PER card
        # example for PCOMP:
        #    {'MID': 2, 'SOUT': 'YES', 'T': 0.023622, 'THETA': 0.0}
        card_subset = dict()
        # card_set: several (at least one) PER card
        # example for PCOMP:
        #   [{'MID': 2, 'SOUT': 'YES', 'T': 0.023622, 'THETA': 0.0},
        #    {'MID': 3, 'SOUT': 'YES', 'T': 0.452756, 'THETA': 0.0},
        #    {'MID': 2, 'SOUT': 'YES', 'T': 0.023622, 'THETA': 0.0}}]
        card_set = []
        # --------------------------------------------------------------------
        # some usefull intermediate variables
        field_nb = self.repeated["starts@"] - 1  # starting field index
        parsed_fields_counter = 0
        # --------------------------------------------------------------
        # we should stop on float if and only if -etc.- is not the last
        # field
        stop_cycling_on_float = "floating" in self.repeated
        while True:  # field_nb < nb_of_fields_to_parse:
            # ----------------------------------------------------------
            # check if end of data to parse is reached
            try:
                # parse next field (if any)
                field_nb += 1
                value = fields[field_nb]
            except:
                # end of job. Well done!
                break
            if stop_cycling_on_float and isinstance(value, float):
                break
            # ----------------------------------------------------------
            # skip continuation fields:
            if field_nb % 10 == 0 or (field_nb - 1) % 10 == 0:
                continue
            # ----------------------------------------------------------
            # get the field name that will be come a fieldname for the `value`
            # already collected
            ix = parsed_fields_counter % len(self.repeated["fields"])
            if ix == 0 and value is None:
                break
            fieldname = self.repeated["fields"][ix]
            parsed_fields_counter += 1
            # ----------------------------------------------------------
            # check default value for repeated stuff
            if value is None:
                value = self.REPEATED_DEFAULTS.get(fieldname, value)
            if fieldname in card_subset:
                # time to change of `card_subset` since we find twice the same key
                card_set.append(card_subset.copy())
                card_subset = {fieldname: value}
            else:
                card_subset[fieldname] = value
        # --------------------------------------------------------------------
        # append last card_subset to set container
        card_set.append(card_subset)
        # check if `card_set` already exists
        container = self.carddata[self.REPEATED_DATA_NAME]
        for i, data in enumerate(container):
            if data == card_set:
                self.carddata["main"][self.REPEATED_DATA_NAME + "ID"].append(i)
                break
        else:
            # nothing existing found
            container.append(card_set)
            self.carddata["main"][self.REPEATED_DATA_NAME + "ID"].append(
                len(container) - 1
            )
        # --------------------------------------------------------------------
        # trailing floating fields (if any)
        floating_fields = self.repeated.get("floating", [])
        for i, fieldname in enumerate(floating_fields):
            try:
                self.carddata["main"][fieldname].append(fields[field_nb + i])
            except:
                # SHALL be in default
                self.carddata["main"][fieldname].append(self.DEFAULTS[fieldname])


class ComplexCard(SimpleCard):
    """Mother Card for specific processing (eg. "PBUSH" and its optional flags)"""

    TABLE = None

    def __init__(self, name=None, data=None):
        super().__init__(name=name, data=data)

    def append_checkin(self, fields):
        """hook triggered right before `append`"""
        return fields

    def append_checkout(self, fields):
        """hook triggered right after `append`"""
        return fields

    def append_fields_list(self, fields):
        fields = self.append_checkin(fields)
        super().append_fields_list(fields)
        self.append_checkout(fields)
