#!/usr/bin/env python

import nltk
from nltk import grammar, parse
import sys
from category import Category, GrammarCategory
import cfg
from semantic_db import SemanticDatabase

class SemanticRuleSet:

    def __init__(self):
        self.parser = None
        self.lexicon = []
        self.syn_sem_dict = {}
        self.productions = []
        self.learned = SemanticDatabase()


    def parse_rule(self, text):
        # Remove the start and end quotes
        tokens = text.split()
        if (len(tokens) > 3 and "'" in text):
            quote_split = text.split("'")
            space_split = text.split()
            tokens = space_split[:2] + [quote_split[1]]

        i = 0
        while i < len(tokens):
            if tokens[i].endswith(",") or tokens[i].endswith(":"):
                replacement = " ".join(tokens[i : i+2])
                tokens[i : i+2] = [replacement]
            else:
                i += 1

        return cfg.Production(GrammarCategory.parse(tokens[0]),
                              map(lambda x: GrammarCategory.parse(x),
                                  tokens[2:]))


    def add_match(self, syntactic_rule, semantic_rule):
        self.parser = None
        if isinstance(syntactic_rule, str):
            syntactic_rule = self.parse_rule(syntactic_rule)
        self.syn_sem_dict[syntactic_rule] = semantic_rule


    def add_rule(self, syntactic_rule, semantic_rule):
        self.parser = None
        # Cast syntactic_rule to a string so that we can properly handle unicode
        # characters and strings.
        syntactic_rule = str(syntactic_rule)
        syntactic_rule = self.parse_rule(syntactic_rule)
        self.add_match(syntactic_rule, semantic_rule)
        self.productions.append(syntactic_rule)


    def add_lexicon_rule(self, lhs, words, func):
        for w in words:
            self.add_rule("%s -> '%s'"%(lhs, w), func)


    def add_lexicon(self, preterminal, terminals):
        self.parser = None
        if isinstance(preterminal, str):
            preterminal = Category.parse(preterminal)
            if not isinstance(preterminal, cfg.Nonterminal):
                preterminal = cfg.Nonterminal(preterminal)
        for terminal in terminals:
            prod = cfg.Production(preterminal, [terminal])
            self.lexicon.append(prod)
            self.productions.append(prod)


    def validate_production_rules(self, productions):
        for prod_rule in productions:
            prod_rule = cleanup_production_rule(p)
            try:
                g = grammar.FeatureGrammar.fromstring(prod_rule)
            except:
                print "ERROR: could not parse the rule:" + prod_rule


    def construct_feature_grammar(self):
        p_str = '\n'.join(map(str, self.productions))
        return grammar.FeatureGrammar.fromstring(p_str)


    def construct_parser(self):
        g = self.construct_feature_grammar()
        self.parser = parse.FeatureEarleyChartParser(g)


    def parse_sentence(self, sentence):
        if self.parser == None:
            self.construct_parser()
        tokens = [token.strip() for token in sentence.split()]
        try:
            trees = self.parser.parse(tokens)
            # deduplicate trees, hashing by string value
            trees = {str(t):t for t in trees}.values()
            return trees
        except:
            return []


    def add_verb(self, form, root, past, present, ppart=None):
        if ppart is None:
            ppart = past
        (pos, proc) = form

        postf = pos.copy()
        postf["tense"] = False

        postt = pos.copy()
        postt["tense"] = True

        self.add_rule(cfg.Production(postf.copy(), [root]),
                      proc(root, False))
        self.add_rule(cfg.Production(postt.copy(), [past]),
                      proc(root, "past"))
        self.add_rule(cfg.Production(postt.copy(), [present]),
                      proc(root, "present"))
        self.add_rule(cfg.Production(GrammarCategory(pos="V_part",
                                                     form=pos["pos"]),
                                    [ppart]),
                      proc(root, "past-participle"))

