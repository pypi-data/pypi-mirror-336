import json
from collections import defaultdict

import nastranio.cards as nio_cards
from nastranio.cards import PROP2ELTS
from nastranio.constants import BOUNDARY

DEFAULT_USERINPUT_TPL = {
    "format": 1,
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
        "materials": {"1": ["MAT1", {"E": 7e6, "NU": 0.33, "RHO": 5000.5}]},
        "properties": {
            1: [
                "PBAR",
                {"MID": 1, "A": 50.0, "I1": 18.0, "I2": 18.0, "J": 0.1, "I12": 0.0},
            ],
            2: [
                "PBUSH",
                {
                    "K": "K",
                    "K1": 1e4,
                    "K2": 1e4,
                    "K3": 1e4,
                    "K4": 1e4,
                    "K5": 1e4,
                    "K6": 1e4,
                },
            ],
            3: ["PSHELL", {"MID1": 1, "T": 3.0, "MID2": 1, "MID3": 1}],
        },
        "affectations": {},
        "boundaries": {},
        "loading": {},
    },
}

DEFAULT_BOUNDARY_INPUT = ["SPC1", {"C": "123456"}]
DEFAULT_LOADING_INPUT = [
    "FORCE",
    {
        "CID": 0,
        "F": 1.0,
        "N1": 1.0,
        "N2": 0.0,
        "N3": 0.0,
        "as_sum": False,
        "exclusive": False,
    },
]


class UserInput:
    def load_parameters(self, parameters):
        self.parameters = parameters
        self.attributes = parameters["attributes"]

    def to_json(self, **kwargs):
        return json.dumps(self.parameters, **kwargs)

    def get_card_data(self, cardname, params, **kwargs):
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
        repeated = fields_info.get("repeated", ())
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
        if repeated:
            ret["repeated"] = repeated
        if unknown:
            ret["unknown"] = {k: v for k, v in params.items() if k in unknown}
        return ret

    def get_materials(self):
        ret = {}
        for mid, (cardname, params) in self.attributes["materials"].items():
            ret[mid] = self.get_card_data(cardname, params, XID=mid)
        return ret

    def get_properties(self):
        ret = {}
        for pid, (cardname, params) in self.attributes["properties"].items():
            ret[pid] = self.get_card_data(cardname, params, XID=pid)
        return ret

    def get_loading(self):
        ret = defaultdict(list)
        for sid, data in self.attributes["loading"].items():
            for grpname, (cardname, params) in data.items():
                _data = self.get_card_data(cardname, params, XID=sid)
                if grpname != "*":
                    _data["over"].append(grpname)
                ret[sid].append(_data)
        return dict(ret)

    def get_boundaries(self):
        ret = defaultdict(list)
        for sid, data in self.attributes["boundaries"].items():
            for grpname, (cardname, params) in data.items():
                _data = self.get_card_data(cardname, params, XID=sid)
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
                _data = self.get_card_data(cardname, params)
                _data["over"] = ["elements", grpname]
                card_by_type[gmsh_elem_type] = _data
            ret[grpname] = card_by_type
        return ret
