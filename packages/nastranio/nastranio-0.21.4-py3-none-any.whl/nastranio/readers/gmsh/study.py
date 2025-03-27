import json
import logging
import shutil
import subprocess
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import yaml

import nastranio.cards as cards
from nastranio.constants import BULK, CASE, COMMENTS, EXEC, META, PARAMS, SUMMARY
from nastranio.readers.gmsh import GmsHParser, user_input
from nastranio.registry import Registry


def _convert_keys_to_int(d: dict):
    """recursively converts dictionnary keys to integer when possible.
    Usefull for json unserialization
    """
    new_dict = {}
    for k, v in d.items():
        try:
            new_key = int(k)
        except ValueError:
            new_key = k
        if type(v) == dict:
            v = _convert_keys_to_int(v)
        new_dict[new_key] = v
    return new_dict


class Study:
    def __init__(self, meshfile, autobuild=True):
        """
        Create a NASTRAN study based on GMSH mesh file.
        If autobuild is True (default), build the NASTRAN model.
        Setting `autobuild` to False allow to intercept GMSH
        mesh for modification (eg. nodes renumbering).
        """
        self._meshfile = Path(meshfile).expanduser()
        self.gmsh = GmsHParser(self._meshfile)
        logging.info("\n" + self.gmsh.info())
        if autobuild:
            self.build()

    def run(self, output="run", exist_ok=True):
        target = self._meshfile.parent / output
        target.mkdir(exist_ok=exist_ok)
        nasfile = target / (self._meshfile.stem + ".nas")
        self.to_nastran(nasfile)
        logging.info(f"wrote {nasfile}")
        MYSTRAN = shutil.which("mystran")
        try:
            subprocess.check_output([MYSTRAN, nasfile], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            logging.error("!!!")
        return target

    def load_user_params(self, params=None):
        """
        `params` can be:
          * a valid dictionnary
          * a path to JSON/YAML parameters file
          * a jsonified string
          * None (in which case, <meshfile>.params.json will be searched for)
        """
        self.ui = user_input.UserInput()
        if isinstance(params, dict):
            return self.load_user_params_from_dict(params)
        # None, string or Path. It may be either a JSON string, either a path
        # to parameters file.
        try:
            self.load_user_params_from_file(params)
        except (FileNotFoundError, OSError):
            self.load_user_params_from_json_txt(params)

    def load_user_params_from_dict(self, dic):
        return self.ui.load_parameters(dic.copy())

    def load_user_params_from_json_txt(self, json_txt, fmt, verbose=True):
        if fmt == ".json":
            params = json.loads(json_txt)
            params = _convert_keys_to_int(params)
        elif fmt in (".yaml", ".yml"):
            params = yaml.load(json_txt, Loader=yaml.FullLoader)
        if verbose:
            print(f"loading configuration from {fmt[1:]} string '{json_txt[:20]}...'")
        return self.load_user_params_from_dict(params)

    def _create_params_file(self, filepath):
        logging.warning(f"create {filepath} template file")
        params_data = self.get_ui_input_template()
        with open(filepath, "w") as fh:
            if filepath.suffix == ".json":
                fh.write(json.dumps(params_data, indent=4, sort_keys=False))
            if filepath.suffix in (".yaml", ".yml"):
                fh.write(yaml.dump(params_data, indent=4, sort_keys=False))

    def load_user_params_from_file(self, filepath, verbose=False):
        if filepath is None:
            extensions = (".json", ".yml", ".yaml")
            for suffix in extensions:
                filepath = self._meshfile.parent / (
                    self._meshfile.stem + ".params" + suffix
                )
                if filepath.exists():
                    break
            else:
                # no parameters file found
                filepath = self._meshfile.parent / (
                    self._meshfile.stem + ".params.json"
                )
                self._create_params_file(filepath)
        with open(filepath, "r") as fh:
            json_txt = fh.read()
        if verbose:
            print(f"loading configuration from {filepath}")
        return self.load_user_params_from_json_txt(
            json_txt, fmt=filepath.suffix, verbose=False
        )

    def orphan_nodes(self, clean=False):
        """delete orphan nodes from GmsH mesh"""
        used_gids = set(self.reg.mesh.gid2eids())
        defined_gids = set(self.gmsh.nodes)
        orphans = defined_gids - used_gids
        if orphans:
            logging.warning(f"{orphans=}")
            if clean:
                for orphan_gid in orphans:
                    self.gmsh.nodes.pop(orphan_gid)
        self.build()

        return orphans

    def get_ui_input_template(self):
        default = self.ui.get_default_template()
        # -------------------------------------------------------------
        # process boundaries. Everything found go to SID 1
        default["attributes"]["boundaries"][1] = {}
        _default_value = self.ui.get_default_boundary_input()
        master_key = "boundaries"
        find_in_grpname = "spc"
        self._update_default_master_key(
            master_key, find_in_grpname, _default_value, default
        )
        # -------------------------------------------------------------
        # process loading.  Everithing found go to SID 1
        default["attributes"]["loading"][1] = {}
        _default_value = self.ui.get_default_loading_input()
        master_key = "loading"
        find_in_grpname = "load"
        self._update_default_master_key(
            master_key, find_in_grpname, _default_value, default
        )
        # -------------------------------------------------------------
        # process affectations
        for dim, grps in self.gmsh.dim2physical_group.items():
            if dim == 0:
                continue
            for grp in grps:
                if dim == 1:
                    default["attributes"]["affectations"][grp.name] = {
                        "PID": 1,
                        "GO/X1": 1.0,
                        "CID": 0,
                        "X2": 0.0,
                        "X3": 0.0,
                    }
                elif dim == 2:
                    default["attributes"]["affectations"][grp.name] = {"PID": 3}
        return default

    def build(self, clean_orphan_nodes=False, bind_mesh_api=True):
        """
        mesh file (.msh)  ━───────┬───────>   NASTRAN BULK
        params file (.yml) ━──────┘
        """
        logging.info("building NASTRAN model")
        if not hasattr(self, "ui"):
            self.load_user_params()
        if clean_orphan_nodes:
            self.orphan_nodes(clean=True)

        self.reg = Registry()
        self.reg.container = {
            META.title: {"source": self._meshfile},
            BULK.title: {},
        }
        self._make_exec()
        self._make_cases()
        self._make_params()
        self._make_materials()
        self._make_properties()
        self._make_boundaries()
        self._make_loading()
        self._make_nodes()
        self._make_elements()
        # finalize registry
        self.reg.bind_mesh_api()
        self.reg._build_summary()

    def to_nastran(self, target=None):
        if not target:
            target = self._meshfile.parent / (self._meshfile.stem + ".nas")
        elif target == str:
            target = None
        return self.reg.to_nastran(target)

    def _update_default_master_key(self, master_key, find, default_value, default):
        all_groups = self.gmsh.physical_groups
        for (grpdim, grpid), grp in all_groups.items():
            if find in grp.name.lower():
                bound = {grp.name: default_value}
                default["attributes"][master_key][1].update(bound)
        # no group was named with SPC, pick-up a random one
        if not default["attributes"][master_key][1]:
            grp = next(iter(all_groups.values()))  # pick up randomly
            bound = {grp.name: default_value}
            default["attributes"][master_key][1].update(bound)

    def _make_nodes(self):
        self.reg.container[BULK.title]["GRID"] = cards.GRID()
        for gid, grid in self.gmsh.nodes.items():
            self.reg.container["bulk"]["GRID"].append_sparams(
                {"ID": gid, "X1": grid.x, "X2": grid.y, "X3": grid.z}
            )

    def _finish_make_items(self, carddata):
        card = carddata["card"]
        cardname = card.__name__
        params = carddata["params"]
        over, grpname = carddata.get("over", (None, None))
        repeat = {}
        if over and (repeated := carddata.get("repeated")):
            if over == "nodes":
                ids = self.gmsh.physical_group2gids[grpname]
            else:
                ids = self.gmsh.physical_group2eids[grpname]
            repeat = {repeated[0]: ids}
        elif repeated := carddata.get("repeated"):
            # eg. PCOMP card has repeated fields without over
            repeat = repeated
        if cardname not in self.reg.container["bulk"]:
            self.reg.container["bulk"][cardname] = card()
        self.reg.bulk[cardname].append_sparams(params, **repeat)

    def _make_materials(self):
        # apply boundaries
        materials = self.ui.get_materials()
        for mid, material in materials.items():
            self._finish_make_items(material)

    def _make_properties(self):
        # apply boundaries
        properties = self.ui.get_properties()
        for pid, prop in properties.items():
            self._finish_make_items(prop)

    def _make_boundaries(self):
        # apply boundaries
        boundaries = self.ui.get_boundaries()
        for sid, constraints in boundaries.items():
            for constraint in constraints:
                self._finish_make_items(constraint)

    def _make_loading(self):
        self._loaded_gids = {}
        # apply boundaries
        loading = self.ui.get_loading()
        for sid, items in loading.items():
            sid2loaded_gids = defaultdict(list)
            self._loaded_gids[sid] = sid2loaded_gids
            for item in items:
                as_sum = item.get("unknown", {}).get("as_sum", False)
                if "over" in item:
                    gids = self.gmsh.physical_group2gids[item["over"][1]]
                    # only FORCE are allowed to be devided
                    if item["card"].__name__ == "FORCE" and as_sum:
                        item["params"]["N1"] /= len(gids)
                        item["params"]["N2"] /= len(gids)
                        item["params"]["N3"] /= len(gids)
                    for gid in gids:
                        _item = deepcopy(item)
                        _item["params"]["G"] = gid
                        _item["missing"].remove("G")
                        sid2loaded_gids[gid].append(_item)
                        # delegate _finish_make_item(_item) to deduplicator
                else:
                    # eg. GRAV
                    self._finish_make_items(item)
            self._loaded_gids[sid] = dict(sid2loaded_gids)
        self._make_loading_inspect_loaded_gids()

    def _make_loading_inspect_loaded_gids(self):
        duplicated_loading = defaultdict(dict)
        for sid, loaded_nodes in self._loaded_gids.items():
            for gid, items in loaded_nodes.items():
                if len(items) > 1:
                    duplicated_loading[sid][gid] = []
                    for item in items:
                        grpname = item["over"][1]
                        is_exclusive = item.get("unknown", {}).get("exclusive", False)
                        duplicated_loading[sid][gid].append((grpname, is_exclusive))
        duplicated_loading = dict(duplicated_loading)
        # ---------------------------------------------------------------------
        # process exclusivity
        if duplicated_loading:
            for sid, gids2loading_grp in list(duplicated_loading.items())[:]:
                for gid, grpnames in gids2loading_grp.copy().items():
                    dedup = defaultdict(set)
                    for grpname, is_exclusive in grpnames:
                        dedup[is_exclusive].add(grpname)
                    if True not in dedup:
                        continue
                    grpname_to_keep = dedup[True]
                    if len(grpname_to_keep) > 1:
                        raise ValueError(
                            f"several exclusivities detected for SID {sid} and GID {gid}: {grpname_to_keep}"
                        )
                    grpname_to_keep = next(iter(grpname_to_keep))
                    # remove unwanted items form _loaded_gids
                    to_pop = []
                    for unwanted_loading_grp in dedup[False]:
                        for i, item in enumerate(self._loaded_gids[sid][gid][:]):
                            item_grpname = item["over"][1]
                            if item_grpname == unwanted_loading_grp:
                                logging.info(
                                    f"loading SID{sid} GRID{gid}: ensure exclusivity for group '{grpname_to_keep}' by removing loading group '{item_grpname}'"
                                )
                                to_pop.append(i)
                    for i in to_pop[::-1]:
                        self._loaded_gids[sid][gid].pop(i)
                        duplicated_loading[sid][gid].pop(i)
                    if len(duplicated_loading[sid][gid]) == 1:
                        duplicated_loading[sid].pop(gid)
        # ---------------------------------------------------------------------
        # create loading
        for sid, loaded_nodes in self._loaded_gids.items():
            for gid, items in loaded_nodes.items():
                for item in items:
                    self._finish_make_items(item)
        # finally clean duplicated_loading
        duplicated_loading = {
            sid: dup for sid, dup in duplicated_loading.items() if dup
        }
        # ---------------------------------------------------------------------
        # feedback
        if duplicated_loading:
            logging.debug(f"{duplicated_loading=}")
            logging.warning("duplicated loading (combined) is detected")
            logging.info("you may want `exclusive` to avoid loads combination.")
            for sid, gids2loading_grp in duplicated_loading.items():
                msg = f"Duplicated loaded grids for SID {sid}:\n"
                for gid, grpnames in gids2loading_grp.items():
                    txt = " & ".join(["'%s'" % grp[0] for grp in grpnames])
                    msg += f"  * GRID {gid}: {txt}\n"
            logging.info(msg)
        self._dup_gids_loading = duplicated_loading

    def _make_elements(self):
        affect = self.ui.get_affectations()
        affected = set()
        for physicalName, item in affect.items():
            eids = self.gmsh.physical_group2eids[physicalName]
            for eid in eids:
                elt = self.gmsh.elements[eid]
                eid_item = deepcopy(item[elt.element_type])
                XID = eid_item["card"].XID_FIELDNAME
                eid_item["params"][XID] = eid
                eid_item["missing"].remove(XID)
                eid_item.pop("over")
                grids = dict(zip(eid_item["card"]._gids_header(), elt.gids))
                eid_item["params"].update(grids)
                eid_item.pop("missing")
                self._finish_make_items(eid_item)
                affected.add(eid)
        # give a feedback about physicalNames not set
        unset = {}
        for physicalName, eids in self.gmsh.physical_group2eids.items():
            nb_unset = len(eids - affected)
            if nb_unset:
                unset[physicalName] = (nb_unset, len(eids))
        for physicalName, (nb_unset, nb_total) in unset.items():
            msg = f"physical group '{physicalName}' has {nb_unset} non-affected elements out of {nb_total}"
            if "spc" not in physicalName.lower() and "load" not in physicalName.lower():
                logging.info(msg)
            else:
                logging.debug(msg)

    def _make_exec(self):
        self.reg.container["exec"] = self.ui.parameters["exec"]

    def _make_cases(self):
        cases = self.ui.parameters["cases"]
        boundary_sids = sorted(list(self.ui.get_boundaries().keys()))
        loading_sids = sorted(list(self.ui.get_loading().keys()))
        default_boundary_sid = boundary_sids.pop(0)
        default_loading_sid = loading_sids[0]
        if len(loading_sids) > 0:
            for sid in loading_sids:
                cases[f"SUBCASE {sid}"] = {
                    "SUBTITLE": f"LCID#{sid}",
                    "SPC": default_boundary_sid,
                    "LOAD": sid,
                }
        else:
            cases["default"]["SPC"] = default_boundary_sid
            cases["default"]["LOAD"] = default_loading_sid
        self.reg.container["cases"] = cases
        pass

    def _make_params(self):
        self.reg.container["params"] = self.ui.parameters["params"]
        pass
