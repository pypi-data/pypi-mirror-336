"""
FEMAP neutral writer
"""

import logging
import os

from jinja2 import Environment, FileSystemLoader
from numtools.intzip import zip_list

TPLPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def _renumber(ints, offset):
    """renumber and return an offseted list of integers and the old->new mapping

    >>> _renumber([1, 2, 3], offset=100)
    ([101, 102, 103], {1: 101, 2: 102, 3: 103})
    >>> _renumber([1, 2, 101], offset=100)
    ([1, 2, 101], {1: 1, 2: 2, 101: 101})
    >>> _renumber([], offset=100)
    ([], {})
    """
    if not ints:
        return [], {}
    _ints = ints.copy()
    if max(ints) < offset:
        ints = [i + offset for i in ints]
    renumbering = dict(zip(_ints, ints))
    return ints, renumbering


_DEFAULT_CLIPPING = (
    #'$COM --- default clipping ---\n'
    "0,0,0,0,0.,0.,\n"  # 4:: coclip:  CC_on, CC_dof, CC_meth, CC_csys, CC_min, CC_max
    "0,0,\n"  # 5:: plcip_meth, plcip_in
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    "0,0,\n"  # 6:: + plclip_on, plclip_neg
    "0.,0.,0.,\n"  #     + plclip_base (X, Y, Z)
    "0.,0.,0.,\n"  #     + plclip_norm (X, Y, Z)
    #'$COM --- /end of default clipping ---\n'
)
FEMAP_ENTITIES = {
    # entity: (group_rule_ID, group_entity_ID)
    "gids": (7, 17),
    "eids": (8, 21),
    "mids": (9, 26),
    "pids": (10, 30),
    "pnt_ids": (1, 3),
    "txt_ids": (5, 14),
}


def _dump_group(group, femap_grp_id, com):
    """
    return a string containing the FEMAP neutral definition for the group.
    """
    # ========================================================================
    # group's header
    # ========================================================================
    str_ = "%s,1,0,\n" % int(femap_grp_id)  # ID, refresh?, no_renumbering?
    str_ += "%s\n" % group["title"]  # group title
    str_ += "0,0,0,\n"  # 3:: min layer, max layer, Type of layer usage
    str_ += _DEFAULT_CLIPPING  # clipping stuff
    # ========================================================================
    # rules
    # ========================================================================
    if com:
        str_ += "$COM --- RULES ---\n"
    str_ += "133,\n"  # MAX number of rules
    for entity, ids, femap_attr in zip(
        group["entities"].keys(), group["entities"].values(), FEMAP_ENTITIES.values()
    ):
        if len(ids) == 0:
            continue
        if com:
            str_ += "$COM --- /%d/ %s ---\n" % (femap_attr[1], entity)
        str_ += "%s,\n" % femap_attr[1]
        items_list = zip_list(ids, couple_alone=0)
        nb_lines = len(items_list)
        if nb_lines > 0:
            tpl = "\n".join(nb_lines * ["%d,%d,1,1,"])
            var = tuple((id_ for e in items_list for id_ in e))
            str_ += tpl % var
            str_ += "\n"
        str_ += "-1,-1,-1,-1,\n"
    str_ += "-1,\n"  # End of rule: last record
    # ========================================================================
    # entities
    # ========================================================================
    if com:
        str_ += "$COM --- ENTITIES ---\n"
    str_ += "28,\n"  # MAX number of entities sets
    # Actual group definition
    for entity, ids, femap_attr in zip(
        group["entities"].keys(), group["entities"].values(), FEMAP_ENTITIES.values()
    ):
        if len(ids) == 0:
            continue
        if com:
            str_ += "$COM --- /%d/ %s ---\n" % (femap_attr[0], entity)
        str_ += "%s,\n" % femap_attr[0]
        nb_lines = len(ids)
        tpl = "\n".join(nb_lines * ["%d,"])
        var = tuple(ids)
        str_ += tpl % var
        str_ += "\n-1,\n"
    # ========================================================================
    # that's all, Folks!
    # ========================================================================
    str_ += "-1,\n"
    return str_


class Neutral(object):
    """
    Class handling basic export to FEMAP neutral file
    """

    default_points_data = {
        "type": 0,
        "engine": 0,
        "csys": 0,
        "layer": 1,
        "color": 22,
        "mesh_size": 0.0,
        "propertyID": 0,
        "compositeCurveID": 0,
    }

    def __init__(self, femap_neutral_vers="11.0", database_title=None):
        self.femap_neu_vers = femap_neutral_vers
        self.database_title = database_title
        # self._create_group_block()
        self.layers = {}  # { Layer ID: ??? }
        # { group ID: {'title': <str>,                               # MANDATORY
        #              'entities':{'eids': set(), 'gids': set()},    # MANDATORY
        #              'reference': [grpID1, grpID2, ...]            # OPTIONAL
        #             }}
        self.groups = {}
        self.texts = {}
        self.ids_offset = 1
        logging.info(f"loading template from {TPLPATH}")
        self.tpl_env = Environment(
            autoescape=False,
            loader=FileSystemLoader(TPLPATH),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _next_id(self, attr):
        ids = set(getattr(self, attr).keys())
        return max(ids, default=self.ids_offset - 1) + 1

    # ========================================================================
    # groups jobs
    # ========================================================================
    def next_group_id(self):
        """return the next available goup id"""
        return self._next_id("groups")

    def add_group(self, title, entities=None, reference=None):
        """
        * 'title': a string defining how the group will be shown in FEMAP
        * 'entities': dictionnary of entities to group ({'eids': ..., 'gids': ...})
        * 'reference': OPTIONAL. iterable of referenced groups
        """
        _entities = dict(zip(FEMAP_ENTITIES.keys(), (set() for i in FEMAP_ENTITIES)))
        if not entities:
            entities = {}
        _entities.update(entities)
        if not reference:
            reference = set()
        nextid = self.next_group_id()
        self.groups[nextid] = {
            "title": title,
            "entities": _entities,
            "reference": reference,
        }
        return nextid

    def refers_groups(self, grpid, grpids):
        """modify an existing group `grpid` to referes some other groups."""
        self.groups[grpid]["reference"] = grpids

    def dump_groups(self, com):
        """write all groups to the neutral file"""
        grpids = sorted(list(self.groups.keys()))
        string = ""
        for grpid in grpids:
            group = self.groups[grpid]
            try:
                string += _dump_group(group, grpid, com)
            except:
                logging.critical(f"cannot dump group ID# {grpid} {group}")
        return string.strip("\n")

    def dump_referenced_groups(self, com):
        msg = ""
        if com:
            msg += "$COM ---[ Referenced Groups ] ---"
        for grpid, group in self.groups.items():
            if "reference" not in group or len(group["reference"]) == 0:
                continue
            msg += "%d\n" % grpid
            msg += ",\n".join(["%d" % g for g in group["reference"]]) + ",\n"
            msg += "-1,\n"
        return msg.strip("\n")

    # ========================================================================
    # layers jobs
    # ========================================================================
    def next_layer_id(self):
        """return the next available goup id"""
        return self._next_id("layers")

    def add_layer(self, title, color=30):
        """add a layer. `layer` is a dictionnary with 2 keys:
        * 'title': a string defining how the group will be shown in FEMAP
        * 'color': OPTIONAL. Defaulted to XXX
        """
        nextid = self.next_layer_id()
        self.layers[nextid] = {"title": title, "color": color}
        return nextid

    def dump_layers(self, com):
        msg = ""
        layers = sorted(self.layers.keys())
        if com:
            msg += "$COM ---[ Layers ] ---"
        for layerID in layers:
            msg += "%d, %d,\n" % (layerID, self.layers[layerID]["color"])
            msg += "%s,\n" % self.layers[layerID]["title"]
        return msg.strip("\n")

    # ========================================================================
    # texts jobs
    # ========================================================================
    def next_text_id(self):
        """return the next available goup id"""
        return self._next_id("texts")

    def add_text(
        self,
        text,
        pointer_loc,
        text_offset=(-1, -1, -1),
        color=124,
        back_color=0,
        bord_color=14,
        font=1,
        layer=1,
        groupID=None,
    ):
        """add a text"""
        data = {
            "text": text,
            "color": color,
            "back_color": back_color,
            "bord_color": bord_color,
            "font": font,
            "layerID": layer,
            "model_positioning": 1,
            "horz_just": 1,  # left
            "vert_just": 0,  # center
            "visible": 1,
            "viewID": 1,
            "draw_pointer": 1,
            "draw_border": 1,
            "pointer_loc": pointer_loc,
            "text_position": [e1 + e2 for e1, e2 in zip(pointer_loc, text_offset)],
            "groupID": groupID,
        }
        nextid = self.next_text_id()
        self.texts[nextid] = data
        if groupID:
            self.groups[groupID]["entities"]["txt_ids"] |= set((nextid,))
        return nextid

    def dump_texts(self):
        """ """
        msg = ""
        txts = self.texts  # .df_text.T.to_dict()
        # prepare template
        tpl = "{txtid:.0f}, {color:.0f}, {back_color:.0f},\
 {bord_color:.0f}, {font:.0f}, {layerID:.0f},\n"
        tpl += "{model_positioning:.0f}, {horz_just:.0f}, {vert_just:.0f},\
 {visible:.0f}, {viewID:.0f}, {draw_pointer:.0f}, {draw_border:.0f},\n"
        tpl += "{tx}, {ty}, {tz},\n"
        tpl += "{px}, {py}, {pz},\n"
        tpl += "{text_lines:.0f},\n"
        tpl += "{text}\n"
        # prepare data
        for txtid, _data in txts.items():
            _data = _data.copy()

            _data["text_lines"] = len(_data["text"].split("\n"))
            _data["txtid"] = txtid
            _loc = _data.pop("text_position")
            _data["tx"] = _loc[0]
            _data["ty"] = _loc[1]
            _data["tz"] = _loc[2]
            _loc = _data.pop("pointer_loc")
            _data["px"] = _loc[0]
            _data["py"] = _loc[1]
            _data["pz"] = _loc[2]
            txt = tpl.format(**_data)
            msg += txt
        return msg.strip("\n")

    # ========================================================================
    # make
    # ========================================================================
    def make(self, com):
        """prepare data for neutral file rendering"""
        data = {
            "com": com,
            # 'database_title': self.database_title,
            "neutral_version": self.femap_neu_vers,
            "layers": self.dump_layers(com=com),
            "groups": self.dump_groups(com=com),
            "referenced_groups": self.dump_referenced_groups(com=com),
            # 'points': self.dump_points(),
            "text": self.dump_texts(),
        }
        return data

    def set_offset(self, offset):
        # apply offset to content
        self.ids_offset = offset
        # --------------------------------------------------------------------
        # renumbering groups
        _, g_renumbering = _renumber(list(self.groups.keys()), offset)
        # self.groups = {g_renumbering[i]: v for i, v in self.groups.items()}
        # also renumber referenced groups
        for grpid, group in self.groups.copy().items():
            newid = g_renumbering[grpid]
            self.groups[newid] = self.groups.pop(grpid)
            assert id(group) == id(self.groups[newid])
            ref = group.get("reference", ())
            if ref:
                logging.info("renumber references for group %d" % newid)
                group["reference"] = [g_renumbering[i] for i in group["reference"]]

        # --------------------------------------------------------------------
        # renumbering layers
        _, l_renumbering = _renumber(list(self.layers.keys()), offset)
        self.layers = {l_renumbering[i]: v for i, v in self.layers.items()}
        # --------------------------------------------------------------------
        # renumbering texts
        _, t_renumbering = _renumber(list(self.texts.keys()), offset)
        for old_text_id, text in self.texts.copy().items():
            new_text_id = t_renumbering[old_text_id]
            self.texts[new_text_id] = self.texts.pop(old_text_id)
            assert id(text) == id(self.texts[new_text_id])
            text["layerID"] = l_renumbering[text["layerID"]]
            if text["groupID"] is not None:
                old_group_id = text["groupID"]
                new_group_id = g_renumbering[text["groupID"]]
                text["groupID"] = new_group_id
                self.groups[new_group_id]["entities"]["txt_ids"].remove(old_text_id)
                self.groups[new_group_id]["entities"]["txt_ids"].add(new_text_id)
        # self.texts = {t_renumbering[i]: v for i, v in self.texts.items()}

    def dump_points(self):
        msg = ""
        pnts = self.model.df_points.T.to_dict()
        pnts = {k + self.ids_offset: v for k, v in pnts.items()}
        string = "{pntid}, {type}, {engine}, {csys}, {layer:.0f}, {color},\
 {mesh_size}, {propertyID}, {compositeCurveID},\n"
        string += "{x}, {y}, {z},\n"
        for pntid, data in pnts.items():
            if pntid == 0:
                continue
            _data = self.default_points_data.copy()
            _data.update(data)
            _data["pntid"] = pntid
            _data["color"] = int(_data["color"]) if _data["color"] else 22
            pnt = string.format(**_data)
            msg += pnt
        return msg.strip("\n")

    # =========================================================================
    # curves
    # =========================================================================
    #    571
    # $com--------------------------
    # 1,28686,0,10004,0,0.,0,0,0,0,0,
    # 0,0,0,
    # 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    # 0.,0.,0.,
    # 0.,0.,0.,0.,0.,0.,
    # 479,480,0,0,0,
    # $com--------------------------
    #    -1

    def get_category_by_grp(self, grp_obj):
        for category, groups in list(self._groups.items()):
            if grp_obj in groups:
                return category

    def write(self, filepath=None, com=False):
        """write the file!"""
        data = self.make(com=com)
        neu = self.tpl_env.get_template("femap_neu.tpl").render(data)
        if not filepath:
            return neu
        with open(filepath, "w") as f:
            f.write(neu)
        return filepath


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
    f = Femap_Neu()
    print(80 * "-")
    print(f.write())
    print(80 * "-")
