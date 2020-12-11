#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from collections import defaultdict
from typing import Dict

class FPNode:
    def __init__(self, name, trans_ids, parent):
        self.name = name
        self.parent = parent
        self.children = dict()
        self.trans_ids = trans_ids
        self.count = len(trans_ids)

    def update_trans_ids(self, trans_ids):
        self.trans_ids.update(trans_ids)
        self.count += len(trans_ids)

    def print_node(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.print_node(ind + 1)
        

class FPTree:
    def __init__(self, item2ids: Dict):
        self.root = FPNode("root", set(), None)
        self.header_table = defaultdict(list)
        self.item2ids = item2ids

    def _insert_item(self, node: FPNode, item, trans_ids):
        if item in node.children:
            child = node.children[item]
            child.update_trans_ids(trans_ids)
        else:
            child = node.children[item] = FPNode(item, trans_ids.copy(), node)
            self.header_table[item].append(child)
        return child

    def insert_trans(self, trans, trans_ids):
        cur_node = self.root
        for item in sorted(trans, key=lambda i: len(self.item2ids[i]), reverse=True):
            cur_node = self._insert_item(cur_node, item, trans_ids)
        
    def find_pattern_base(self, item):
        cond_pattern_base = list()
        for node in self.header_table[item]:
            prefix_path = list()
            cur_node = node.parent
            while cur_node and cur_node is not self.root:
                prefix_path.append(cur_node.name)
                cur_node = cur_node.parent
            cond_pattern_base.append((frozenset(prefix_path), node.trans_ids))
        return cond_pattern_base

    def is_single_path(self):
        cur_node = self.root
        while True:
            if len(cur_node.children) > 1:
                return False
            if len(cur_node.children) == 0:
                break
            cur_node = list(cur_node.children.values)[0]
        return True

    def sort_header_table(self):
        self.header_table = dict(sorted(self.header_table.items(), key=lambda pair: len(self.item2ids[pair[0]])))

def create_tree(trans_db, min_support):
    item2ids = defaultdict(set)
    for trans, ids in trans_db:
        for item in trans:
            item2ids[item].update(ids)
    # remove items whose support is less than min_sup
    for item, ids in list(item2ids.items()):
        if len(ids) < min_support:
            del(item2ids[item])

    tree = FPTree(item2ids)

    freq_items = set(item2ids.keys())
    if len(freq_items) == 0:
        return tree
    
    for trans, ids in trans_db:
        trans = trans & freq_items
        tree.insert_trans(trans, ids)
    tree.sort_header_table()
    return tree
