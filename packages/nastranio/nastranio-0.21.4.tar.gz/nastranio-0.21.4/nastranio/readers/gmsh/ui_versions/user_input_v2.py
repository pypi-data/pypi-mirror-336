import json
import logging
from collections import defaultdict
from copy import deepcopy

import yaml

import nastranio.cards as nio_cards
from nastranio.cards import PROP2ELTS
from nastranio.constants import BOUNDARY

DEFAULT_USERINPUT_TPL = {
    "format": 2,
    "exec": {"SOL": "SESTATIC"},
    "params": {
        "PRGPST": "YES",
        "POST": -1,
        "OGEOM": "NO",
        "AUTOSPC": "YES",
        "K6ROT": 100.0,
        "GRDPNT": 0,
        "SKIPMGG": "YES",
        "CHKGRDS": "NO",
    },
    "cases": {
        "default": {
            "id": -1,
            "TITLE": "LCID1",
            "ECHO": "NONE",
            "DISPLACEMENT(PLOT)": "ALL",
            "$ SPC": 1,
            "$ LOAD": 1,
        }
    },
    "attributes": {
        "materials": {
            1: {"card": "MAT1", "params": {"E": 7e6, "NU": 0.33, "RHO": 5000.5}},
            2: {"card": "MAT1", "params": {"E": 8e6, "NU": 0.33, "RHO": 5000.5}},
        },
        "properties": {
            1: {
                "card": "PBAR",
                "params": {
                    "MID": 1,
                    "A": 50.0,
                    "I1": 18.0,
                    "I2": 18.0,
                    "J": 0.1,
                    "I12": 0.0,
                },
            },
            2: {
                "card": "PBUSH",
                "params": {
                    "K": "K",
                    "K1": 1e4,
                    "K2": 1e4,
                    "K3": 1e4,
                    "K4": 1e4,
                    "K5": 1e4,
                    "K6": 1e4,
                },
            },
            3: {
                "card": "PSHELL",
                "params": {"MID1": 1, "T": 3.0, "MID2": 1, "MID3": 1},
            },
            4: {
                "card": "PCOMP",
                "params": {
                    "NSM": 0.0,
                },
                "layup": [
                    {"MID": 1, "SOUT": "YES", "T": 0.018, "THETA": 0.0},
                    {"MID": 2, "SOUT": "YES", "T": 0.339, "THETA": 0.0},
                    {"MID": 1, "SOUT": "YES", "T": 0.018, "THETA": 5.0},
                ],
            },
        },
        "affectations": {},
        "boundaries": {},
        "loading": {},
    },
}

DEFAULT_BOUNDARY_INPUT = {"card": "SPC1", "params": {"C": "123456"}}
DEFAULT_LOADING_INPUT = {
    "card": "FORCE",
    "params": {
        "CID": 0,
        "F": 1.0,
        "N1": 1.0,
        "N2": 0.0,
        "N3": 0.0,
        "as_sum": False,
        "exclusive": False,
    },
}


def _from_v1_carddata(carddata):
    """
    was [<cardname>, <params>]
    now {"card": <cardname>, "params": <params>}
    """
    try:
        return {"card": carddata[0], "params": carddata[1]}
    except:
        logging.critical(f"cannot import {carddata} from V1")


def from_v1(parameters):
    parameters = deepcopy(parameters)
    parameters["format"] = 2
    for section_name in ("materials", "properties"):
        section = parameters["attributes"][section_name]
        for entry_id, carddata in section.items():
            parameters["attributes"][section_name][entry_id] = _from_v1_carddata(
                carddata
            )
    for section_name in ("boundaries", "loading"):
        section = parameters["attributes"][section_name]
        for sid, group2carddata in section.items():
            for grpname, carddata in group2carddata.items():
                parameters["attributes"][section_name][sid][grpname] = (
                    _from_v1_carddata(carddata)
                )
    return parameters


class UserInput:
    def load_parameters(self, parameters):
        convmap = {1: from_v1}
        format = parameters["format"]
        if format != DEFAULT_USERINPUT_TPL["format"]:
            logging.warning(f"importing from deprecated {format=}")
            parameters = convmap[format](parameters)
            self.imported_from = format
        else:
            self.imported_from = None
        self.parameters = parameters
        self.attributes = parameters["attributes"]

    def get_default_template(self):
        return deepcopy(DEFAULT_USERINPUT_TPL)

    def get_default_boundary_input(self):
        return deepcopy(DEFAULT_BOUNDARY_INPUT)

    def get_default_loading_input(self):
        return deepcopy(DEFAULT_LOADING_INPUT)

    def to_json(self, filepath=None, indent=2, sort_keys=False, **kwargs):
        txt = json.dumps(self.parameters, indent=indent, sort_keys=sort_keys, **kwargs)
        if filepath:
            with open(filepath, "w") as fh:
                fh.write(txt)
            return filepath
        return txt

    def to_yaml(self, filepath=None, indent=2, sort_keys=False, **kwargs):
        txt = yaml.dump(self.parameters, sort_keys=sort_keys, **kwargs)
        if filepath:
            with open(filepath, "w") as fh:
                fh.write(txt)
            return filepath
        return txt

    def get_card_data(self, carddata, **kwargs):
        """merge user input with card definition"""
        cardname = carddata["card"]
        params = carddata["params"]
        card = getattr(nio_cards, cardname)
        params = params.copy()
        if "XID" in kwargs:
            kwargs[card.XID_FIELDNAME] = kwargs.pop("XID")
        params.update(kwargs)
        fields_info = card.fields_info()
        mandatory = set(fields_info["mandatory"])
        optional = fields_info["optional"]
        all = mandatory | optional
        unknown = set(params) - all
        missing = mandatory - set(params)
        ok_params = {k: v for k, v in params.items() if k in all}
        ret = {
            "card": card,
            "params": ok_params,
        }
        if hasattr(card, "LOADING_TYPE") and card.LOADING_TYPE is not None:
            ret["over"] = [card.LOADING_TYPE]
        if card.type == BOUNDARY:
            ret["over"] = ["nodes"]
        if missing:
            ret["missing"] = missing
        # ---------------------------------------------------------------------
        # repeated fields
        repeated = fields_info.get("repeated", ())
        # if cardname == "PCOMP":
        #     breakpoint()
        if repeated:
            repeated_data_raw = carddata.get(card.REPEATED_DATA_NAME)
            if repeated_data_raw is None:
                # SPC1 has a REPEATED_DATA_NAME, but not available at this point
                ret["repeated"] = repeated
            else:
                # PCOMP has a REPEATED_DATA_NAME, and data are available
                repeated_data = defaultdict(list)
                for data in repeated_data_raw:
                    for fieldname, value in data.items():
                        repeated_data[fieldname + "i"].append(value)
                ret["repeated"] = dict(repeated_data)
        if unknown:
            ret["unknown"] = {k: v for k, v in params.items() if k in unknown}
        # eg for PCOMP:
        # {
        #  'card': <class 'nastranio.cards.properties.PCOMP'>,
        #  'params': {'NSM': 0.0, 'PID': 4},
        #  'repeated': {'MIDi': [1, 1, 1],
        #            'THETAi': [0.0, 90.0, 0.0],
        #            'Ti': [0.01, 0.05, 0.01]},

        return ret

    def get_materials(self):
        ret = {}
        for mid, carddata in self.attributes["materials"].items():
            ret[mid] = self.get_card_data(carddata, XID=mid)
        return ret

    def get_properties(self):
        """
        return a dictionnary with cards specifications:

        (Pdb++) pp(ret)
        {1: {'card': <class 'nastranio.cards.properties.PBAR'>,
             'params': {'A': 1.0, 'I1': 12.0, 'I2': 13.0, 'MID': 1, 'PID': 1}},
         2: {'card': <class 'nastranio.cards.properties.PSHELL'>,
             'params': {'MID1': 1, 'MID2': 1, 'MID3': 1, 'PID': 2, 'T': 0.08}},
         3: {'card': <class 'nastranio.cards.properties.PSHELL'>,
             'params': {'MID1': 1, 'MID2': 1, 'MID3': 1, 'PID': 3, 'T': 0.03}},
         4: {'card': <class 'nastranio.cards.properties.PCOMP'>,
             'params': {'NSM': 0.0, 'PID': 4},
             'repeated': {'MIDi': [1, 1, 1],
                          'THETAi': [0.0, 90.0, 0.0],
                          'Ti': [0.01, 0.05, 0.01]}}}
        """
        ret = {}
        for pid, carddata in self.attributes["properties"].items():
            ret[pid] = self.get_card_data(carddata, XID=pid)
        return ret

    def get_loading(self):
        ret = defaultdict(list)
        for sid, data in self.attributes["loading"].items():
            for grpname, carddata in data.items():
                _data = self.get_card_data(carddata, XID=sid)
                if grpname != "*":
                    _data["over"].append(grpname)
                ret[sid].append(_data)
        return dict(ret)

    def get_boundaries(self):
        ret = defaultdict(list)
        for sid, data in self.attributes["boundaries"].items():
            for grpname, carddata in data.items():
                _data = self.get_card_data(carddata, XID=sid)
                if grpname != "*":
                    _data["over"].append(grpname)
                ret[sid].append(_data)
        return dict(ret)

    def get_affectations(self):
        ret = {}
        props = self.get_properties()
        for grpname, params in self.attributes["affectations"].items():
            prop_card = props[params["PID"]]["card"]
            cards_choice = PROP2ELTS[prop_card.__name__]
            card_by_type = {}
            for cardname in cards_choice:
                gmsh_elem_type = getattr(nio_cards, cardname).gmsh_eltype
                _data = self.get_card_data(
                    carddata={"card": cardname, "params": params}
                )
                _data["over"] = ["elements", grpname]
                card_by_type[gmsh_elem_type] = _data
            ret[grpname] = card_by_type
        return ret
