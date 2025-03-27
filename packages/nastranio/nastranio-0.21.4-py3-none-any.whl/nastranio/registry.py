import json
import logging
import os
import re
from collections import defaultdict, namedtuple
from multiprocessing import Manager, Process
from pathlib import Path

from numtools.serializer import Serializer

from nastranio import cards as cards_mod
from nastranio.constants import (
    BULK,
    CASE,
    COMMENTS,
    EXEC,
    META,
    PARAMS,
    SUMMARY,
    UNKNOWN,
)
from nastranio.decorators import timeit
from nastranio.mesh_api import Mesh
from nastranio.mesh_api.mod import Mod
from nastranio.readers.bulk import read_buffer, read_bulk
from nastranio.utils import calcdiff

# ----------------------------------------------------------------------------
# optional imports...

# fmt: off
try:
    import msgpack
    ISMSGPACK = True
except ImportError:
    ISMSGPACK = False
    logging.debug('`msgpack` not available')

try:
    from deepdiff import DeepDiff
    ISDEEPDIFF = True
except ImportError:
    ISDEEPDIFF = False
    logging.debug('`deepdiff` not available')
# fmt: on


class Registry(Serializer):
    """
    Main public entry point to Nastran Bulk file parsing.
    """

    def __init__(self):
        self.container = None

    def _build_summary(self):
        """(re-)build from scratch a summary dict. Use full when
        registry is manually created
        """
        _summary = defaultdict(set)
        for cardname, card in self.container["bulk"].items():
            _summary[card.type].add(cardname)
            if hasattr(card, "shape"):
                _summary[card.shape].add(cardname)
            if hasattr(card, "dim"):
                _summary[card.dim].add(cardname)
        self.container["summary"] = dict(_summary)

    def diff(self, other, exclude_meta=False):
        return calcdiff((self.container, other.container), exclude_meta=exclude_meta)

    def __eq__(self, other):
        diff = calcdiff((self.container, other.container), exclude_meta=True)
        return len(diff) == 0

    def comments(self):
        """associate cards individuals to comments"""
        # --------------------------------------------------------------------
        # search for FEMAP comments
        if COMMENTS.title not in self.container:
            return {}
        comments = self.container[COMMENTS.title]
        femap_tags = defaultdict(dict)
        regex = re.compile(
            r"^\$\s+Femap\s*(?P<what>(\w+\s+)+)\s*(?P<id>\d+)\s*:\s*(?P<title>.*)$"
        )
        for coms in comments:
            # skip block comment
            for com in coms.split("\n"):
                # if "\n" in com:
                #     continue
                m = regex.match(com)
                if m:
                    femap_tags[m.group("what").replace("with NX Nastran", "").strip()][
                        int(m.group("id"))
                    ] = m.group("title").strip()
        return dict(femap_tags)

    def check_consistancy(self, verbose=True):
        """introspect myself and display some useful infos and warnings"""
        issues = []
        # --------------------------------------------------------------------
        # warning on unknown cards
        ucards = list(self.container.get("summary", {}).get(UNKNOWN, ()))
        if ucards:
            issues.append(("warning", "Unknown cards: %s" % ucards))
        if verbose:
            for level, msg in issues:
                getattr(logging, level)(msg)
        return issues

    def bind_mesh_api(self):
        self.mesh = Mesh()
        self.mesh.set_registry(self, calc_csys=True)

    def bind_mod_api(self, index_elems=("0d", "1d", "2d", "3d")):
        """bind nastranio.mesh_api.mod.Mod class"""
        self.mesh.mod = Mod()
        self.mesh.mod.set_registry(self, index_elems=index_elems)
        logging.info("Modification Module loaded under `reg.mesh.mod`")

    # ========================================================================
    # input / output
    # ========================================================================

    # ------------------------------------------------------------------------
    # NASTRAN BULKFILES

    def from_bulkfile(self, filename, nbprocs="auto", progress=True):
        """Populate a registry from a NASTRAN bulk file"""
        self.container = None
        try:
            fh = filename
            fh.seek(0)
            if nbprocs not in ("auto",) and nbprocs > 1:
                logging.warning("reading filelike object is monoproc")
            containers = read_buffer(fh, progress=progress)
        except AttributeError:
            containers = read_bulk(
                filename=filename, nbprocs=nbprocs, progress=progress
            )
        self.container = containers.pop(0)
        for cont in containers:
            self._merge_container(cont)
        # create self.container['bulk'] dictionnaries:
        self.bind_mesh_api()
        # =====================================================================
        # write all grids to CSYS 0
        # =====================================================================
        modgids = self._translate_grids_to_0()
        if modgids:
            logging.warning("translated {len(modgids)} nodes to CSYS0}")
        self.check_consistancy()

    def _translate_grids_to_0(self):
        """
        ensure IDs described in carddata are in the same order as
        IDs got from  GRID.coords()
        """
        if len(self.container["bulk"]["GRID"]) == 0:
            return set()
        if set(self.container["bulk"]["GRID"].carddata["main"]["CP"]) == set((0,)):
            return set()
        coordsK = self.container["bulk"]["GRID"].coords(asdf=True)  # as defined
        coords0 = self.container["bulk"]["GRID"].coords(
            csysreg=self.mesh.CSys, incsys=-1
        )  # coordinates in CSYS0
        gcdata = self.container["bulk"]["GRID"].carddata["main"]
        ids = gcdata["ID"]
        ids_coords = coords0[0]
        assert list(ids_coords) == ids
        gids_to_modify = coordsK[coordsK["csys"] != 0].index
        for gid in gids_to_modify:
            rowno = self.container["bulk"]["GRID"]._id2rowno[gid]
            gcdata["CP"][rowno] = 0
            xyz0 = coords0[1][rowno]
            gcdata["X1"][rowno] = xyz0[0]
            gcdata["X2"][rowno] = xyz0[1]
            gcdata["X3"][rowno] = xyz0[2]
        self.container["bulk"]["GRID"].clear_caches()
        return set(gids_to_modify)

    def to_nastran(self, filename=None):
        """dumps registry to NASTRAN deck file"""
        bulk = ""
        # ---------------------------------------------------------------------
        # EXEC
        if "exec" in self.container:
            for k, v in self.container["exec"].items():
                bulk += f"{k} {v} \n"
            bulk += "CEND\n"
        # ---------------------------------------------------------------------
        # CASES
        if "cases" in self.container:
            for case_section, data in self.container["cases"].items():
                if case_section != "default":
                    bulk += f"{case_section}\n"
                for k, v in data.items():
                    if k.isupper():
                        bulk += f"  {k} = {v}\n"
        # ---------------------------------------------------------------------
        # BULK (parameters)
        if "param" in self.container or "bulk" in self.container:
            bulk += "BEGIN BULK\n"
        for param, value in self.container.get("params", {}).items():
            bulk += f"PARAM,{param},{value}\n"
        # ---------------------------------------------------------------------
        # BULK (data)
        for cardfamily, cards in self.container.get("bulk", {}).items():
            bulk += "\n".join(cards.to_nastran(comments=self.comments()))
            bulk += "\n"
        # ---------------------------------------------------------------------
        # end
        bulk += "ENDDATA"
        if filename:
            filename = Path(filename).expanduser()
            with open(filename, "w") as fh:
                fh.write(bulk)
            return filename
        return bulk

    # ------------------------------------------------------------------------
    # from / to file

    def from_file(self, fname, fmt="auto"):
        """unserialize registry from a msgpack or json file"""
        if fmt == "auto":
            # guess file type from extension
            fmt = os.path.splitext(fname)[-1][1:]  # "toto.json -> "json"
        self.container = None
        if fmt == "json":
            with open(fname, "r") as fh:
                txt = fh.read()
            self.from_json(txt)

        elif fmt == "pack":
            with open(fname, "rb") as fh:
                txt = fh.read()
            self.from_msgpack(txt)
        else:
            raise ValueError(f"extension/format {fmt} not handled")
        self.check_consistancy()

    def to_file(self, fname=None, fmt="pack"):
        """
        Serialize registry to file. Default is to save to msgpack.

        :param fname: file path
        :type fname: str or `None`
        :param fmt: file's format (and extension)
        :type fmt: str or `None`

        :returns: actual file name
        """
        if not fname:
            # if filename is not provided, save registry besides source file
            # using the passed format `fmt` as extension.
            source = self.meta["source"]
            fname, ext = os.path.splitext(source)
            fname += f".{fmt}"
        if fmt == "json":
            with open(fname, "w") as fh:
                fh.write(self.to_json())
        elif fmt == "pack":
            with open(fname, "wb") as fh:
                fh.write(self.to_msgpack())
        return fname

    def __getattr__(self, attr):
        """
        user-friendly method to access self.container
        """
        # if attr in self.__dict__:
        #     return getattr(self, attr)
        if attr in self.container:
            # logging.debug('proxy to self.container["%s"]', attr)
            return self.container[attr]
        for section, data in self.container.items():
            if attr in data:
                # logging.debug('proxy to self.container["%s"]["%s"]', section, attr)
                return self.container[section][attr]
        raise AttributeError(attr)

    def __getstate__(self):
        return {"container": self.container}

    def __setstate__(self, state):
        self.__dict__ = state
        self.bind_mesh_api()
        # if self.container:
        #     self.check_consistancy()

    def _merge_container(self, container):
        """merge two containers into the same registry.
        use full for multiprocess resuming
        """
        sections = (EXEC, PARAMS, CASE, COMMENTS, BULK, SUMMARY)
        for section in sections:
            if section.title not in container:
                continue
            # if section.title in (EXEC.title, PARAMS.title, CASE.title):
            #     # only bulk and comments should be non-zero
            #     if len(container[section.title]) != 0:
            #         logging.debug("%s::%s", section.title, BULK.title)
            #         raise ValueError("Section {0.title} not empty".format(section))
            if section.title not in self.container:
                self.container[section.title] = {}
            self_d = self.container[section.title]
            other_d = container[section.title]
            logging.debug(f"merge {section.title} (%d items)", len(other_d))
            if section.title in (EXEC.title, PARAMS.title, CASE.title):
                self_d.update(other_d)
            elif section.title == COMMENTS.title:
                # reglar lists
                self_d += other_d
            elif section.title == SUMMARY.title:
                for k in other_d:
                    self_d[k] |= other_d[k]
            elif section.title == BULK.title:
                # append new bulk cards_mod family to self
                for bulk_entry, bulk_entries in container[BULK.title].items():
                    if bulk_entry not in self.container[BULK.title]:
                        self.container[BULK.title][bulk_entry] = bulk_entries
                        logging.debug(
                            'added "%s" (%d items)', bulk_entry, len(bulk_entries)
                        )
                        continue
                    # entry already exists ; we need to append entries
                    else:
                        self.container[BULK.title][bulk_entry].merge(bulk_entries)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
