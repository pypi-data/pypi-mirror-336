import logging
from functools import wraps

from numtools.intzip import hzip


class Modificator:
    """GmsHParser mixin class dedicated to modification"""

    def post_init(self):
        if not hasattr(self, "_locked_gids"):
            self._locked_gids = set()

    def lock_gids(self, gids):
        if isinstance(gids, (int, float)):
            gids = set((gids,))
        self._locked_gids |= set(gids)

    def renumber_nodes(self, /, mapping_in, lockin):
        """renumber nodes based on a mapping_in {current_node_id -> new_node_id}"""
        self.post_init()

        booked_gids = set(self.nodes)

        def _get_free_id():
            newgid = max(booked_gids) + 1
            booked_gids.add(newgid)
            return newgid

        # discard non-existing nodes from requirements
        mapping_in = {n1: n2 for n1, n2 in mapping_in.items() if n1 in self.nodes}
        logging.info(f"requested {mapping_in=}")
        # discard locked nodes
        forbidden = set(mapping_in) & self._locked_gids
        if forbidden:
            logging.warning(
                f"gids {hzip(forbidden)} are locked. They won't be renumbered"
            )
        mapping_in = {n1: n2 for n1, n2 in mapping_in.items() if n1 not in forbidden}
        # split dic_target into mapping_in , dic_back such
        buffer = {}
        temp_way_back = {}
        for n_source, n_target in mapping_in.items():
            intermediate_gid = _get_free_id()
            buffer[n_source] = intermediate_gid
            temp_way_back[intermediate_gid] = n_target
            if n_target in self.nodes:
                if n_target not in buffer:
                    intermediate_gid = _get_free_id()
                    buffer[n_target] = intermediate_gid
                    # temp_way_back[intermediate_gid] = intermediate_gid  # we may forget this one
                else:
                    pass
        way_back = {}
        for k, v in temp_way_back.items():
            if k not in buffer.values():
                continue
            way_back[k] = v
        assert sorted(list(set(way_back.values()))) == sorted(list(way_back.values()))
        assert sorted(list(set(buffer.values()))) == sorted(list(buffer.values()))
        mapping = {}
        for k, v in buffer.copy().items():
            mapping[k] = way_back.get(v, v)
            # if mapping[k] == k:
            #    buffer.pop(k, None)
            #    way_back.pop(k, None)
            #    mapping.pop(k, None)
        self._renumber_apply_mapping(buffer)
        self._renumber_apply_mapping(way_back)
        # provide appropriate executed mapping
        if lockin:
            to_lock = set(mapping_in.values())
            self._locked_gids |= to_lock
            logging.info(f"locked gids {hzip(to_lock)}")
        return mapping

    def _renumber_apply_mapping(self, dic):
        # reassign elements
        # print(f"apply {dic}")
        elts_to_modify = set()
        modified_elts = set()
        for n1 in dic:
            elts_to_modify = self.gid2eids[n1]
            # logging.info(f"node {n1} is used by {elts_to_modify}")
            for eid in elts_to_modify:
                elt = self.elements[eid]
                ix = elt.gids.index(n1)
                gids = list(elt.gids)
                gids[ix] = dic[n1]
                elt = elt._replace(gids=tuple(gids))
                self.elements[eid] = elt
                modified_elts.add(eid)
        # logging.info(f"modified elements {modified_elts}")
        # renumber nodes
        nodes_buffer = {}
        for gid, newgid in dic.items():
            node = self.nodes.pop(gid)
            node = node._replace(gid=newgid)
            nodes_buffer[newgid] = node
        self.nodes.update(nodes_buffer)
        self._make_gid_eid_type()
        self._make_eid_gid_physicalGroups()
        return modified_elts

    def renumber_nodes_by_grp(self, physical_name, startat=1, lockin=False):
        gids = self.physical_group2gids[physical_name]
        targets = list(range(startat, startat + len(gids) + 1))
        mapping = dict(zip(gids, targets))
        return self.renumber_nodes(mapping_in=mapping, lockin=lockin)

    def renumber_nodes_offset(self, offset, lockin=False):
        mapping = {k: k + offset for k in self.nodes}
        return self.renumber_nodes(mapping_in=mapping, lockin=lockin)
