#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from collections import defaultdict
import math
import itertools

from .fptree import FPTree, create_tree


def fpgrowth(tree: FPTree, min_sup, prefix):
    for base, _ in tree.header_table.items():
        freq_itemset = prefix.copy()
        freq_itemset.add(base)
        yield (freq_itemset, tree.item2ids[base])
        
        pattern_base = tree.find_pattern_base(base)
        local_tree = create_tree(pattern_base, min_sup)
        if len(local_tree.header_table) > 0:
            yield from fpgrowth(local_tree, min_sup, freq_itemset)

def mine_fp(db, min_sup):
    '''
    Return: generator of tuple like `(freq_itemset, support_trans_ids)`

    '''
    if isinstance(min_sup, float) and (0 < min_sup < 1):
        min_sup = min_sup * len(db)
    min_sup = math.ceil(min_sup)

    trans2ids = defaultdict(set)
    for trans_id, trans in enumerate(db):
        trans2ids[frozenset(trans)].add(trans_id)
    trans_db = list(trans2ids.items())

    tree = create_tree(trans_db, min_sup)
    yield from fpgrowth(tree, min_sup, set())

