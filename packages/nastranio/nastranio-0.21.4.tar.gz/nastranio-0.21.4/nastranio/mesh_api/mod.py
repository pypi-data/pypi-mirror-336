"""Mesh Modification package"""

import logging
import numbers
from collections import defaultdict

import numpy as np
from numpy.lib import recfunctions as rfn

import nastranio.cards as cards
from nastranio.mesh_api.rtree_indexes import RTrees
from nastranio.utils import project_point, project_point_fast


class Mod:
    def set_registry(self, registry, index_elems=("0d", "1d", "2d", "3d")):
        self.reg = registry
        self.bulk = registry.container["bulk"]
        self.mesh = registry.mesh
        self.rtrees = RTrees(registry, index_elems=index_elems)
        self.rtrees.build()

    def node_move_to(self, gid, coords):
        """move node `gid` to new coordinates"""
        logging.info(f"move gid{gid} to {coords}")
        griddata, rowno = self.bulk["GRID"].query_id(gid, with_loc=True)
        rowno = rowno[0][0]
        grid_coords = np.array(coords)
        old_grid_coords = rfn.structured_to_unstructured(griddata[["X1", "X2", "X3"]])
        old_grid_coords = old_grid_coords[0]
        # collect current (pre-mod) impacted elements bboxes
        impacted_eids = self.reg.mesh.gid2eids(gids=(gid,))[gid]
        premod_elts_bboxes = {
            eid: self.reg.mesh.get_eid_bbox(eid) for eid in impacted_eids
        }
        logging.debug(f"move gid#{gid} from {old_grid_coords}")
        logging.debug(f"     to {grid_coords=}")
        logging.debug(f"     {rowno=}")
        logging.debug(f"     impacted elts bboxes={premod_elts_bboxes.keys()}")
        # =====================================================================
        # update mesh
        # =====================================================================
        # change GRID carddata
        self.bulk["GRID"].carddata["main"]["X1"][rowno] = grid_coords[0]
        self.bulk["GRID"].carddata["main"]["X2"][rowno] = grid_coords[1]
        self.bulk["GRID"].carddata["main"]["X3"][rowno] = grid_coords[2]
        # ---------------------------------------------------------------------
        # rebuild caches
        self.bulk["GRID"].clear_caches()
        # =====================================================================
        # update rtrees
        # =====================================================================
        self.rtrees.update_grid(gid, old_coords=old_grid_coords, coords=grid_coords)
        for eid, old_coords in premod_elts_bboxes.items():
            coords = self.reg.mesh.get_eid_bbox(eid)
            logging.info(f"moved {gid} from {old_coords} to {coords}")
            self.rtrees.update_element(eid, old_coords=old_coords, coords=coords)

    def node_move_by(self, gid, vector):
        """move node `gid` by vector"""
        logging.info("move gid{gid} by vector {coords}")
        griddata, rowno = self.bulk["GRID"].query_id(gid, with_loc=True)
        vector = np.array(vector)
        old_coords = rfn.structured_to_unstructured(griddata[["X1", "X2", "X3"]])[0]
        coords = old_coords + vector
        logging.debug(f"move gid#{gid} by vector={vector}")
        logging.debug(f"     from {old_coords=} to {coords=}")
        return self.node_move_to(gid, coords=coords)

    def node_add(self, coords, gid=None, clear_caches=False):
        """add grid <gid> at provided coords"""
        if not gid:
            gid = self.mesh.next_unused_gid()
        else:
            # check that node gid does not exist
            if gid in self.mesh.gid2eids():
                raise ValueError(f"node {gid} already exists")
        # ---------------------------------------------------------------------
        # update registry
        self.reg.container["bulk"]["GRID"].append_sparams(
            {"ID": gid, "X1": coords[0], "X2": coords[1], "X3": coords[2]}
        )
        # ---------------------------------------------------------------------
        # update rtree
        self.rtrees.add_grid(gid, coords=coords)
        # ---------------------------------------------------------------------
        # clear caches
        if clear_caches:
            self.bulk["GRID"].clear_caches()
        return gid

    def force_define_subcase(self, lcid, spcid=1, title=None):
        if not title:
            title = f"LCID#{lcid} SPC#{spcid}"
        lcid_key = f"SUBCASE {lcid}"
        cases = self.reg.container["cases"]
        if lcid_key not in cases:
            cases[lcid_key] = {
                "SUBTITLE": title,
                "SPC": spcid,
                "LOAD": lcid,
            }

    def force_add(
        self,
        lcid,
        gid,
        scale=1.0,
        fx=0.0,
        fy=0.0,
        fz=0.0,
        mx=0.0,
        my=0.0,
        mz=0.0,
        lcid_title=None,
        clear_caches=False,
    ):
        for f in ("FORCE", "MOMENT"):
            if f not in self.reg.container["bulk"]:
                self.reg.container["bulk"][f] = getattr(cards, f)()
        # ---------------------------------------------------------------------
        # update registry
        self.reg.container["bulk"]["FORCE"].append_sparams(
            {"SID": lcid, "G": gid, "CID": 0, "F": scale, "N1": fx, "N2": fy, "N3": fz}
        )
        self.reg.container["bulk"]["MOMENT"].append_sparams(
            {"SID": lcid, "G": gid, "CID": 0, "M": scale, "N1": mx, "N2": my, "N3": mz}
        )

        if clear_caches:
            self.bulk["FORCE"].clear_caches()
            self.bulk["MOMENT"].clear_caches()

    def force_clear_caches(self):
        self.bulk["FORCE"].clear_caches()
        self.bulk["MOMENT"].clear_caches()

    def elem1d_split(
        self,
        eid,
        where,
        rtree=None,
        new_gid=None,
        replicate_pins=False,
        clear_caches=False,
    ):
        """
        split 1d element:
            * if where is a 0<where<1 number, use it as relative length
            * if `where` is a list of numbers, assume it as new location

        If `replicate_pins` is `False` (default`), then:
            * existing element PB is set to None
            * new element PA is set to None
            * new element PB is set to initial element PB

        If `replicate_pins` is `True` (default is `False`), then new
        new element has the same PIN FLAGS `"PA"` and `"PB"` than
        initial element


        """
        cardname = self.reg.mesh.eid2card(skipcache=True)[eid]
        card = self.reg.container["bulk"][cardname]
        if isinstance(where, numbers.Number):
            if not 0 < where < 1:
                raise ValueError(f"`where` ({where}) must be in ]0,1[ range.")
            # ---------------------------------------------------------------------
            # find location of split
            _gid_a, _gid_b = self.reg.mesh.eid2gids(eids=(eid,), keep_order=True)[eid]
            _length = self.reg.mesh.length(eids=(eid,))["data"][0]
            _offset = self.reg.mesh.normals().loc[eid] * where * _length
            _base_point = (
                self.bulk["GRID"].coords(asdf=True)[["X", "Y", "Z"]].loc[_gid_a]
            )
            new_gid_coords = (_base_point + _offset).to_list()
        else:
            # assume a list/tuple of numbers is passed
            new_gid_coords = where
        initial_eid_bbox = self.reg.mesh.get_eid_bbox(eid)
        # ---------------------------------------------------------------------
        # create gid
        new_gid = self.node_add(gid=new_gid, coords=new_gid_coords, clear_caches=False)
        self.rtrees.add_grid(new_gid, coords=new_gid_coords)
        # ---------------------------------------------------------------------
        # change final node of existing element
        # copy property from initial element
        eid_ix, old_gid = card.update_gid(eid=eid, gidno=1, new_gid=new_gid)
        old_properties = {k: v[eid_ix] for k, v in card.carddata["main"].items()}
        new_properties = old_properties.copy()
        # ---------------------------------------------------------------------
        # create new element
        new_eid = self.mesh.next_unused_eid()
        gids_header = card.gids_header
        new_properties[card.XID_FIELDNAME] = new_eid
        new_properties[gids_header[0]] = new_gid
        new_properties[gids_header[1]] = old_gid
        # ---------------------------------------------------------------------
        # if `not replicate_pins` only keep defined pins
        if not replicate_pins:
            pina, pinb = old_properties["PA"], old_properties["PB"]
            if pina or pinb:
                card.carddata["main"]["PB"][eid_ix] = None
                new_properties["PA"] = None
                new_properties["PB"] = pinb
        self.reg.container["bulk"][card.name].append_sparams(new_properties)
        # ---------------------------------------------------------------------
        # update rtree
        bbox = self.reg.mesh.get_eid_bbox(eid=new_eid)
        self.rtrees.add_elem(cardname, new_eid, coords=bbox, rtree=rtree)
        self.rtrees.update_element(
            eid,
            old_coords=initial_eid_bbox,
            coords=self.reg.mesh.get_eid_bbox(eid=eid),
            rtree=rtree,
        )
        # ---------------------------------------------------------------------
        # clear caches
        if clear_caches:
            self.bulk["GRID"].clear_caches()
            card.clear_caches()
            self.reg.mesh.clear_caches()
        return card, new_eid, new_gid

    def multiple_elem1d_split(
        self,
        points,
        cardname=None,
        rtree=None,
        eids=None,
        margin=0.01,
        round_t_digits=None,
    ):
        """split elements found close to each point"""
        if eids:
            rtree = self.reg.mesh.mod.rtrees.create_rtree(eids=eids)
        if not round_t_digits:
            # round `t` to number of digits of margin, therefore, defaulted to 2
            round_t_digits = len(str(float(margin)).split(".")[-1])
        _details = []
        _historic_by_eid = defaultdict(list)
        _prev_eids = defaultdict(set)
        for i, point in enumerate(points):
            prev_eids = self.rtrees.nearest_elements(
                point, cardname=cardname, rtree=rtree, astype=list
            )
            prev_eid = next(iter(prev_eids))
            if cardname:
                cardnames = (cardname,)
            geoms = self.mesh.geom_1d_elements(cardnames=cardnames)
            elt = geoms.loc[prev_eid]
            ga = elt[["XA", "YA", "ZA"]].values
            gb = elt[["XB", "YB", "ZB"]].values
            proj, t = project_point_fast(point, ga, gb)
            # -----------------------------------------------------------------
            # if t == 0 or == 1, len(prev_eids) should be >1
            if margin < t < (1 - margin):
                point = proj
                card, new_eid, new_gid = self.elem1d_split(
                    eid=prev_eid, where=point, clear_caches=False, rtree=rtree
                )
            else:
                if t < margin:
                    new_gid = int(elt["GA"])
                    point = elt[["XA", "YA", "ZA"]].tolist()
                    t = 0
                else:
                    new_gid = int(elt["GB"])
                    point = elt[["XB", "YB", "ZB"]].tolist()
                    t = 1
                new_eid = None
            # -----------------------------------------------------------------
            # keep track of initial element
            if new_eid:
                # if a new element has been created, append it to the list of
                # old element children
                for root_eid, _eids_ in _prev_eids.items():
                    if prev_eid in _eids_:
                        break
                else:
                    # nothing found. It's an element that hasn't been already split
                    root_eid = prev_eid
                _prev_eids[root_eid].add(new_eid)
            else:
                # no element split. An existing node is returned, so, let's return the
                # existing element as mother and child element
                root_eid = prev_eid
                new_eid = prev_eid
                # but maybe prev_eid comes from a previous plit...?
            _historic_by_eid[new_eid].append(root_eid)
            __details = {
                "prev_eids": _historic_by_eid[new_eid],  # ths whole historic
                "prev_eid": root_eid,  # really the last one
                "eid": new_eid,
                "gid": new_gid,
                "XA": point[0],
                "XB": point[1],
                "XC": point[2],
                "t": round(t, round_t_digits),
            }
            _details.append(__details)
        # -----------------------------------------------------------------
        # rebuild caches
        self.bulk["GRID"].clear_caches()
        card = self.reg.container["bulk"][cardname]
        card.clear_caches()
        self.reg.mesh.clear_caches()
        return _details
