import json
import logging
from base64 import b64decode, b64encode

try:
    import msgpack

    ISMSGPACK = True
except ImportError:
    ISMSGPACK = False
import pickle

from nastranio import cards as cards_mod


class PythonObjectEncoder(json.JSONEncoder):
    """encode sets to json"""

    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        if hasattr(obj, "to_json"):
            # serialize cards
            return {"_nastran_card": obj.to_json()}
        return {"_python_object": b64encode(pickle.dumps(obj)).decode("utf-8")}


def as_python_object(dct):
    if "_python_object" in dct:
        return pickle.loads(b64decode(dct["_python_object"].encode("utf-8")))
    if "_nastran_card" in dct:
        # resurrect nastran card
        _data = json.loads(dct["_nastran_card"])
        cardname = _data["card"]
        card = cards_mod.__dict__.get(cardname, cards_mod.DefaultCard)(name=cardname)
        card.resume(_data)
        return card
    return dct


def msgpack_encode(obj):
    if isinstance(obj, set):
        obj = {"__set__": True, "as_list": list(obj)}
    elif hasattr(obj, "to_msgpack"):
        # serialize cards
        obj = {"__msgpack__": True, "as_msg": obj.to_msgpack()}
    return obj


def msgpack_decode(obj):
    if "__msgpack__" in obj:
        _data = msgpack.unpackb(obj["as_msg"], raw=False, object_hook=msgpack_decode)
        cardname = _data["card"]
        card = cards_mod.__dict__.get(cardname, cards_mod.DefaultCard)(name=cardname)
        card.resume(_data)
        return card
    elif "__set__" in obj:
        obj = set(obj["as_list"])
    return obj
