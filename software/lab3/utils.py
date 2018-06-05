"""
Utility functions for this lab.
"""

from copy import deepcopy

from nltk.tree import Tree
from nltk.featstruct import Feature

#from lambda_interpreter import lambdastr

##############################################################################

def is_leaf_node(tree_node):
    return not isinstance(tree_node, Tree)


def deconstruct_featstruct(fs):
    node_type, node_entries = None, []
    
    for k, v in fs.iteritems():
        if isinstance(k, Feature):
            if k.name == 'type':
                assert node_type == None
                node_type = v
        elif isinstance(k, unicode):
            if isinstance(v, bool):
                node_entries.append(('+' if v else '-') + k)
            elif isinstance(v, str):
                node_entries.append("%s='%s'"%(k, v))

    assert node_type != None
    return (node_type, node_entries)


def featstruct_to_str_repr(fs, include_feats=True):
    node_type, node_entries = deconstruct_featstruct(fs)
    if include_feats == False or len(node_entries) == 0:
        return node_type
    else:
        return "%s%s"%(node_type, "[%s]"%(", ".join(node_entries)))


def node_to_str_repr(node, include_feats=True):
    if is_leaf_node(node):
        return "'%s'"%(node)
    else:
        return featstruct_to_str_repr(node.label(), include_feats)


def node_to_str_rule_repr(node, include_feats=True):
    lhs = node_to_str_repr(node, include_feats)
    if is_leaf_node(node):
        return lhs
    rhs = " ".join([node_to_str_repr(c, include_feats)
                    for c in node])
    return "%s -> %s"%(lhs, rhs)


def walk_tree(tree,
              leaf_func=lambda x: None,
              pre_nonleaf_func=lambda x: None,
              post_nonleaf_func=lambda x: None):
    """
    Depth-First traversal of the tree.
    """
    tree = deepcopy(tree)

    def walk(node):
        # Depth First Traversal of an NLTK Tree.
        if is_leaf_node(node):
            leaf_func(node)
        else:
            pre_nonleaf_func(node)
            if len(node) > 0:
                for child in node:
                    walk(child)
            post_nonleaf_func(node)

    walk(tree)
    return tree
