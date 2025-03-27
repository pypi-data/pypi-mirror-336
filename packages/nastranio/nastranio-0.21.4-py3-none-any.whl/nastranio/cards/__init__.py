import ast
import glob
import os
from collections import defaultdict

from nastranio.cards.axis import *
from nastranio.cards.elements import *
from nastranio.cards.loading import *
from nastranio.cards.materials import *
from nastranio.cards.properties import *
from nastranio.cardslib import SimpleCard
from nastranio.constants import CARDS_REGISTER, ELEMENT, PROPERTY

ELT2PROPS = None
PROP2ELTS = None


def collection():
    """
    return collection of cards as a set
    """
    return frozenset(CARDS_REGISTER)


def associate():
    """create nastranio.cards.e2c and nastranio.cards.c2e dictionnaries"""
    from nastranio.cards import elements, properties

    global ELT2PROPS, PROP2ELTS
    ELT2PROPS = {}
    PROP2ELTS = defaultdict(set)
    property_cards = {
        c: card
        for c in collection()
        if (
            hasattr(properties, c) and (card := getattr(properties, c)).type == PROPERTY
        )
    }
    element_cards = {
        c: card
        for c in collection()
        if (hasattr(elements, c) and (card := getattr(elements, c)).type == ELEMENT)
    }
    _exclusive_c2p = {}
    for cardname in collection():
        try:
            card = getattr(elements, cardname)
        except AttributeError:
            continue
        if card.type == ELEMENT:
            # check if we have a property by name
            prop_candidate = f"P{cardname[1:]}"
            if prop_candidate in property_cards:
                props = set((prop_candidate,))
                _exclusive_c2p[cardname] = prop_candidate
            else:
                # get by dimension, if property card has PID field
                props = {
                    _cardname
                    for _cardname, pcard in property_cards.items()
                    if (
                        pcard.DIM == card.dim
                        and hasattr(card, "PID_FIELDNAME")
                        and f"C{_cardname[1:]}" not in element_cards
                    )
                }
            ELT2PROPS[cardname] = props
            for prop in props:
                PROP2ELTS[prop].add(cardname)
    PROP2ELTS = dict(PROP2ELTS)


class DefaultCard(SimpleCard):
    """default container for unknow cards"""

    def append_fields_list(self, fields):
        """fields are provided as text, without the card name"""
        # insert TWO dummy fields such as index in fields list match NASTRAN field
        fields = ["", ""] + fields
        # ==================================================================
        # read fixed fields
        # ==================================================================
        _fields = {}
        nb_appended = max([len(v) for v in self.carddata["main"].values()], default=0)
        for ix, value in enumerate(fields):
            header = f"field#{ix}"
            if header not in self.carddata["main"] and nb_appended > 0:
                # maybe first time this fields is appended
                # we need to create a list full of None
                self.carddata["main"][header] = [None] * nb_appended
            self.carddata["main"][header].append(value)
            _fields[ix] = header
        _fields = {
            k: v for k, v in _fields.items() if (k % 10 != 0 and (k - 1) % 10 != 0)
        }
        self.fields.update(_fields)
        return fields


associate()
