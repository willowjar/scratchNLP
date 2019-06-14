"""
Utility functions for matching the productions from lab_rules
with the (implicit) productions extracted from the feature chart.
"""

from nltk.featstruct import Feature

from category import Category
from lab3.utils import is_leaf_node, walk_tree, node_to_str_repr
from lambda_interpreter import lambdastr

def match_terminal(terminal, term):
    if type(terminal) is str:
        terminal = unicode(terminal)
    if type(term) is str:
        term = unicode(term)
    #print("is terminal ", terminal, term)
    assert type(terminal) == type(term)
    return terminal == term


def match_nonterminal(nonterminal, term):
    # term has <= as many features in nonterminal
    num_matched_features = 0

    # Check that the category / name matches
    for k, v in nonterminal.iteritems():
        if isinstance(k, Feature):
            if k.name == 'type':
                # Check for matching categories
                if isinstance(term, Category):
                    if term.head() != v:
                        return False
                elif term['pos'] != v:
                    return False

    # Check that the features match
    nonterm_slash = False

    for k, v in nonterminal.iteritems():
        if isinstance(k, Feature):
            if k.name == 'type':
                continue # Handled above
            elif k.name == 'slash':
                # No slash
                if v == False:
                    if term['/'] != False:
                        return False
                else:
                    # There is a slash, check that it is the same
                    if '/' not in term.keys():
                        return False
                    if term['/'] == False:
                        return False
                    if term['/']['pos'] != v.items()[0][1]:
                        return False
                    nonterm_slash = True
            else:
                assert False, k.name
        elif isinstance(k, unicode):
            if isinstance(v, bool):
                if k in term.keys():
                    if v != term[k]:
                        return False
                    num_matched_features += 1
            elif isinstance(v, str):
                if k in term.keys():
                    assert type(term[k]) == type(v)
                    if v != term[k]:
                        return False
            else:
                assert False, repr((k, v))
        else:
            assert False

    if type(term['/']) != bool:
        if term['/'] != None:
            if nonterm_slash == False:
                return False

    if not isinstance(term, Category):
        term_features = filter(lambda k: k not in ('/', 'pos'),
                               term.keys())
        num_term_features = len(term_features)
        if num_matched_features != num_term_features:
            return False

    return True


def match_node(node, term):
    if type(term) == str:
        return match_terminal(node, term)
    elif type(term) == unicode:
        assert False, repr((node, term))
    else:
        return match_nonterminal(node.label(), term)


def match_rule(node, production_rule):
    # Match left hand side
    lhs_node = node
    if not match_nonterminal(lhs_node.label(),
                             production_rule.lhs()):
        return False

    # Match right hand side
    rhs_nodes = [c for c in node]
    rhs_prods = production_rule.rhs()

    if len(rhs_nodes) != len(rhs_prods):
        return False
    return all([match_node(n, p)
                for n, p in zip(rhs_nodes, rhs_prods)])


def find_matching_productions(node, sem_rule_set):
    matching_prods = [p for p in sem_rule_set.productions if match_rule(node, p)]
    for rule in matching_prods:
        assert rule in sem_rule_set.syn_sem_dict, rule
    return matching_prods


def decorate_parse_tree(tree, sem_rule_set, set_productions_to_labels=False):
    """
    Given a parse tree, traverse it and match each node to a production rule
    from the grammar and its associated lambda form.
    """
    prod_rules = []

    def decorate(node):
        # tina look here
        if not is_leaf_node(node):
            matching_rules = find_matching_productions(node, sem_rule_set)

            assert 0 < len(matching_rules)

            if 1 < len(matching_rules):
                # It's ok to match more than rule if they all map to the same
                # lambda form.
                set_of_rules = set([lambdastr(sem_rule_set.syn_sem_dict[rule])
                                    for rule in matching_rules])
                assert len(set_of_rules) == 1, set_of_rules

            prod_rules.append((node, matching_rules))
        node.matched_production = matching_rules[0]
        if set_productions_to_labels:
            node.set_label(node_to_str_repr(node))

    decorated_tree = walk_tree(tree, pre_nonleaf_func=decorate)
    return decorated_tree
