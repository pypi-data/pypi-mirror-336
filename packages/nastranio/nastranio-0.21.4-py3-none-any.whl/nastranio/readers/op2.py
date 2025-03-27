"""
interface with OP2 results
"""

# ============================================================================
# ⚠ NOTE ⚠
# ----------------------------------------------------------------------------
# For now, use pyNastran
# ----------------------------------------------------------------------------
# nic@alcazar -- lundi 2 décembre 2019, 14:08:12 (UTC+0100)
# mercurial: 36fcd4a16748 tip
# ============================================================================

import glob
import logging
import multiprocessing as mp
import os
import time

import numpy as np
import pandas as pd

try:
    from pyNastran.op2.op2 import OP2
except ImportError as exc:
    logging.warning("pyNastran not installed.")
    import sys

    sys.exit(0)  # make pytest fails..
from nastranio.utils import chained_dot

PD_OPTIONS = {"precision": 3}
NP_PRINTOPTIONS = {"precision": 3, "threshold": 20}


def set_options(pd_options=None, np_printoptions=None):
    if not pd_options:
        pd_options = PD_OPTIONS
    for k, v in pd_options.items():
        pd.set_option(k, v)
    if not np_printoptions:
        np_printoptions = NP_PRINTOPTIONS
    for k, v in np_printoptions.items():
        np.set_printoptions(**np_printoptions)


class MultipleOP2:
    """basic wrapper around pyNastran OP2 cls"""

    def __init__(self, mode="nx", autorename=True):
        self._mode = mode
        self._autorename = autorename
        self.subcases = {}
        # automatic renaming for DataFrames columns headers
        self._op2nasca = {
            "lc": "lc",
            "NodeID": "gid",
            "ElementID": "eid",
            "ElementType": "source",
            "f1": "t1",
            "f2": "t2",
            "f3": "t3",
            "m1": "r1",
            "m2": "r2",
            "m3": "r3",
            "t12": "shear_xy_mat",
            "t1z": "shear_xz_mat",
            "t2z": "shear_yz_mat",
            "NodeID": "gid",
            "ElementID": "eid",
            "Item": "vector",
            "Layer": "ply_id",
            0: "FEA_value",
        }
        self._nasca2op = {v: k for k, v in self._op2nasca.items()}

    def _new_op2(self, debug=False, log=None, debug_file=None):
        """op2 boilerplate"""
        op2 = OP2(debug=debug, log=log, debug_file=debug_file)
        op2.set_mode(self._mode)
        return op2

    @property
    def lcs(self):
        return self.subcases.copy()

    def read_op2(self, args):
        """read a single op2. Can be called multiple times"""
        if isinstance(args, str):
            multiprocess = False
            filename = args
        else:
            multiprocess = True
            filename = args[0]
            container = args[1]
        fname, ext = os.path.splitext(filename)
        rootdir, _ = os.path.split(filename)
        op2 = self._new_op2()
        op2.read_op2(
            filename, combine=True, build_dataframe=False, skip_undefined_matrices=True
        )
        if not multiprocess:
            # single process reading
            # get last id from subcases
            try:
                id_offset = max(self.subcases.keys())
            except:
                id_offset = 0
            for isubcase in op2.subcase_key.keys():
                self.subcases[isubcase + id_offset] = (op2, isubcase, op2.title)
        else:
            container.append((filename, op2, tuple(op2.subcase_key.keys())))

    def read_op2_in_dir(self, path, pattern="*.op2", multiprocess=False):
        """
        Read several op2 from dir, as per provided pattern. Default (``'*.op2'``) is to
        read all op2 from path."""
        files = glob.glob(os.path.join(path, pattern))
        files = sorted(files)
        start = time.time()
        if not multiprocess:
            for file in files:
                self.read_op2(file)
            stop = time.time()
        else:
            # multiprocess reading
            with mp.Manager() as manager:
                op2s = manager.list()
                args = [(file, op2s) for file in files]
                with manager.Pool() as pool:
                    pool.map(self.read_op2, args)
                op2s = list(op2s)
            # sort op2s by filename
            op2s = sorted(op2s, key=lambda x: x[0])
            offset = 0
            for fname, op2, lcids in op2s:
                for isubcase in lcids:
                    self.subcases[isubcase + offset] = (op2, isubcase, op2.title)
                offset += len(lcids)
            stop = time.time()
        logging.info(70 * "-")
        logging.info("read %d files in %.3f sec." % (len(files), stop - start))
        logging.info(70 * "-")

    def release_df(self, df):
        """post-processing function for released DataFrames"""
        if self._autorename:
            df = df.reset_index().rename(columns=self._op2nasca)
            cols = [c for c in df.columns if not c.startswith("level_")]
            df = df[cols]
            df.columns.name = None
            return df
        return df.reset_index()

    def available_results(self):
        """derived from
        site-packages/pyNastran/.../op2_results.py
        """
        # get first load case
        lcid, (op2, isubcase, title) = next(iter(self.subcases.items()))
        op2.op2_results._get_base_objects_map()
        # ---------------------------------------------------------------------
        # comments
        sum_obj_map = op2.op2_results._get_sum_objects_map()
        from collections import defaultdict

        available = defaultdict(list)
        for key, obj in sum_obj_map.items():
            sub_results = obj.get_table_types()
            msgi = ""
            for sub_result in sub_results:
                unused_base, sub_result2 = sub_result.split(".")
                res = getattr(obj, sub_result2)
                if res is None or res == {}:
                    continue
                available[key].append(sub_result2)
        # available = {"force": ["cbar_force", "ctria3_force"], ...}
        vector2object = {}
        for typ, vectors in available.items():
            for vector in vectors:
                vector2object[vector] = f"{typ}.{vector}"
        return dict(vector2object)

    def result(self, attr, filter_v=None, autoclean=True):
        """read one single result from all op2s and all subcases,
        and return a dataframe
        """
        _res = {}
        vector2object = self.available_results()
        for lcid, (op2, isubcase, title) in self.subcases.items():
            logging.info(
                f'recover "{attr}" for lcid {lcid} "{title}" (isubcase={isubcase})',
                end="...",
            )
            # res = getattr(op2.op2_results.stress, attr)

            if attr not in ("displacements",):
                attr_ = vector2object.get(attr)
                if not attr_:
                    logging.info("no results. Return")
                    return
                res = chained_dot(op2.op2_results, attr_)
            else:
                res = getattr(op2, attr)
            res = res.get(isubcase)
            if not res:
                logging.info("no results. Return")
                return
            if res.dataframe is None:
                res.build_dataframe()
            res = res.dataframe.copy().reset_index()
            if filter_v:
                res = res[res[list(filter_v.keys())].isin(filter_v).all(axis=1)]
            _res[lcid] = res
            logging.info("ok")
        _res = pd.concat(_res, axis=0)
        _res.index.names = ["lc"] + _res.index.names[1:]
        if autoclean:
            return self.release_df(_res)
        return _res

    def results(self, attrs, filter_v=None):
        """sequential `self.result()`` calls"""
        dfs = [self.result(attr, filter_v=filter_v, autoclean=False) for attr in attrs]
        # eventually remove Nones
        dfs = [df for df in dfs if df is not None]
        df = pd.concat(dfs)
        return self.release_df(df)

    def gpf(self, filter_v=None):
        """
        read 'grid_point_forces'
        """
        filter_v = self._translate_filter(filter_v)
        return self.result("grid_point_forces", filter_v=filter_v)

    def composites(self, filter_v=None):
        """"""
        attrs = (
            "cquad4_composite_stress",
            "ctria3_composite_stress",
            "cquad8_composite_stress",
        )
        filter_v = self._translate_filter(filter_v)
        df = self.results(attrs, filter_v=filter_v)
        return df

    def _translate_filter(self, filter_v):
        if not filter_v:
            return
        translated = {}
        for k, values in filter_v.items():
            values = [self._nasca2op.get(v, v) for v in values]
            translated[self._nasca2op.get(k, k)] = values
        return translated
