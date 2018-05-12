# -*- coding: utf-8 -*-

import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry

####################################################################

def translate(data):
    pass

def translateModifier(data):
    pass

####################################################################

identity = lambda x: x

sem = SemanticRuleSet()

####################################################################
# Speech Actions
def processSentence(data):
    return {"scripts": [[111, 146, data ]]}

def soundCommand(name):
    print("soudncomannd called")
    return [["playSound:", name]]

def ynQuestion(data):
    if sem.learned.yesno_query(data):
        return "Yes."
    else:
        return "No."

def whQuestion(data):
    results = sem.learned.wh_query(data)
    if len(results) == 0:
        return "I don't know."
    else:
        return list(results)[0]


def npOnlyHuhResponse(data):
    return "What about %s?"%(pretty_print_entry(data))


####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))

# Sound Command
sem.add_rule("S -> AL", lambda al: identity)
sem.add_rule("AL -> AP", lambda ap: identity)
sem.add_rule("AP -> SoundCommand", lambda sc: identity)
sem.add_rule("SoundCommand -> 'play' 'the' NAME_OF_SOUND 'sound' ", lambda play, the, name, sound: soundCommand(name))

####################################################################
## Lexicon

# Names
sem.add_lexicon_rule("NAME_OF_SOUND",
                     ['meow'],
                     lambda name: identity)

# # Common nouns
# sem.add_lexicon_rule("N[-mass, number=singular]",
#                      ['book', 'city', 'dog', 'man', 'park', 'woman', 'country'],
#                      lambda word: lambda det, apstar:\
#                          C("Object", type=word, definite=det, mod=apstar))


# # Determiners
# sem.add_lexicon_rule("Det",
#                      ['the', 'this'],
#                      lambda word: True)

# sem.add_lexicon_rule("Det",
#                      ['a', 'an'],
#                      lambda word: False)


##############################################################################
# Now we will run the rules you are adding to solve problems in this lab.
import my_rules
my_rules.add_my_rules(sem)
