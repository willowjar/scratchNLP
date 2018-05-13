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
program = []

####################################################################
# Speech Actions
def processSentence(data):
    return {"scripts": [[111, 146, data ]]}

def soundCommand(name):
    return ["playSound:", name]
def singleCommand(commandName, value):
    print("commandName, value",commandName, value)
    return [commandName, value]

def singleCommandNoValue(comandName):
    return [commandName]

def ifCommand(if_cond, if_body):
    return ["doIf", if_cond, [if_body]]
    
def ifElseCommand(if_cond, if_body, else_body):
    return ["doIfElse", if_cond, [if_body],[else_body]]
    
def repeat(num_times, repeat_body):
    return ["doRepeat", num_times, [repeat_body]]
def until(until_condition, repeat_body):
    return ["doUntil", until_condition, [repeat_body]]
def doForever(forever_body):
    return ["doForever", [forever_body]]
def deleteClone():
    return ["deleteClone"]
    
  
def wait(wait_time):
    return ["wait:elapsed:from:", wait_time]
def waitUntil(until_condition):
    return ["doWaitUntil", until_condition]
    
def setVariable(var_name, value):
    return ["setVar:to:", value]
    
def deleteVariable(variable_name):
    # TODO: modify project.json to delete variable from sprite
    # Should return nothing or empty string?
    pass
    
def createClone():
    print("creating clone")
    return ["createCloneOf:", "myself"]
    
def createVariable(vl):
    ## to do
    pass
def createList(name):
    ## to do
    pass
    
def itemInList(unk, name):
    return ["list:contains:", name, unk]
    
def resetTimer():
    return ["timerReset"]

def Dur(np):
    if np == -1:
        return [["doForever"]]
    return [["doRepeat:", np]]
   
# OPERATORS
def add(n1, n2):
    return ['+', n1, n2]

def subtract(n1, n2):
    return ['-', n1, n2]

def getProduct(num, num2):
    return ["*", num, num2]

def getQuotient(num, num2):
    return ["/", num, num2]

def getValue(var):
    return ["readVariable", var_name]

def getRandomNumberBetween(unk1, unk2):
    return ['randomFrom:to:', unk1, unk2]
    
def lessThan(a,b):
    return ["<", a, b]
    
def greaterThan(a,b):
    return [">", a, b]
    
def equalTo(a,b):
    return ["=", a, b]

def GEQ(a,b):
    return ["|", [">", a, b], ["=", a, b]]
    ## CHECK BRACKETS
def LEQ(a,b):
    return ["|", ["<", a, b], ["=", a, b]]
    ## CHECK BRACKETS
    
def logicOr(b1, b2):
    return ["|", b1, b2]

def logicAnd(b1, b2):
    return ["&", b1, b2]

def waitTillTimer(x):
    ["doWaitUntil", x] 

def changeVarBy(var_name, unk, opt_negate=False):
    if opt_negate:
        return ["changeVar:by:", var1, ["*", unk, -1]]
    return ["changeVar:by:",var_name, unk]
    
def changeVarbyVar(var1, var2,opt_negate=False):
    if opt_negate:
        return ["setVar:to:", var1, ["*", getValue(var2), -1]]
    return ["changeVar:by:", var1, getValue(var2)]

def ynQuestion(data):
    if sem.learned.yesno_query(data):
        return "Yes."
    else:
        return "No."
        
def whenGreenFlag():
    return ["whenGreenFlag"]
    
def whenKeyClicked(name):
    return ["whenKeyPressed", name]
    
def whenClicked():
    return ["whenClicked"]

def whenBackSwitch(name):
    return ["whenSceneStarts", name]
    
def whenReceive(message):
    return ["whenIReceive", message]
    
def broadcastMessage(name):
    return ["broadcast:", name]

def broadCastMessageWait(name):
    return ["doBroadcastAndWait:", name]

def not_identity(x):
    return ["not", x]

def SimpleEvent(e, a):
    return [e, a]

def whQuestion(data):
    results = sem.learned.wh_query(data)
    if len(results) == 0:
        return "I don't know."
    else:
        return list(results)[0]

def npOnlyHuhResponse(data):
    return "What about %s?"%(pretty_print_entry(data))

# List commands
def getItem(ind, list_name):
    return ['getLine:ofList:', ind, list_name]

def wordMap(order_adverb):
    adverbToNumMap = {
        'firstly': 1,
        'first': 1,
        'second': 2,
        'secondly': 2,
        'third': 3,
        'thirdly': 3,
        'fourth': 4,
        'fourthly': 4,
        'fifth': 5,
        'fifthly': 5,
        'sixth': 6,
        'sixthly': 6,
        'seventh': 7}
    return adverbToNumMap[order_adverb]
    
def addToList(list_name, item):
    return [['append:toList:', item, list_name]]
    
def deleteListItem(list_name, ind):
    return [['deleteLine:ofList:', ind, list_name]]
    
def setItemInList(ind, list_name, item):
    return [['setLine:ofList:to:', ind, list_name, item]]
    
# Loop commands
def repeat_action_list(action_list, duration):
    if duration == 'forever':
        return [['doForever', action_list]]
    else: 
        return [['doRepeat', duration, action_list]]

def get_duration(durationPhrase):
    if durationPhrase == 'forever':
        return durationPhrase
    else:
        # TODO: unsure about this
        return (text2num(durationPhrase.split()[0]))
    
# Sequential commands
def appendToProgram(action_list):
    #TODO: figure out when we append to the program
    program.append(action_list)
    

####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))

# All Command
sem.add_rule("S -> AL", identity)
sem.add_rule("AL -> AP", identity)
sem.add_rule("AL -> AP AL", lambda p, l: [p] + l) # CHECK IF RIGHT WAY TO CREATE LIST OF ACTIONS
sem.add_rule("AL -> AP 'and' AL", lambda p,an, l: [p] + l) # CHECK IF RIGHT WAY TO CREATE LIST OF ACTIONS
sem.add_rule("AP -> SoundCommand", identity)
sem.add_rule("AP -> CreateCommand", identity)
sem.add_rule("AP -> DataCommand", identity)
sem.add_rule("AP -> EventHandler", identity)
sem.add_rule("AP -> OrderedCommand", identity)
sem.add_rule("AP -> SequentialCommand", identity)
sem.add_rule("AP -> ConditionalCommand", identity)
sem.add_rule("AP -> LoopCommand", identity)
sem.add_rule("AP -> OperatorCommand", identity)
sem.add_rule("AP -> TimerCommand", identity)
sem.add_rule("AP -> BroadcastCommand", identity)
sem.add_rule("AP -> ControlCommand", identity)
sem.add_rule("OrderedCommand -> OrderAdverb AL", lambda num, al: al)

# SequentialCommand
sem.add_rule("SequentialCommand -> SequenceAdverb AL", lambda seq_adv, action_list: appendToProgram(action_list))

# Create Command
sem.add_rule("CreateCommand -> create a clone of myself", createClone())
sem.add_rule("CreateCommand -> 'make' Var VARIABLE_LIST", lambda make, x, vl: createVariable(vl))

sem.add_rule("CreateCommand -> 'make' Lis LIST_NAME 'for' 'a' 'single' 'sprite'", lambda make, lis, name, fr, a, single, sprite: createList(name))
sem.add_rule("CreateCommand -> 'make' Lis LIST_NAME", lambda make, lis, name: createList(name))
sem.add_rule("CreateCommand -> 'make' Lis LIST_NAME 'for' 'all' 'the' 'sprites'", lambda make, lis, name, fr, al, the, sprites: createList(name))

sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME", lambda vl: [vl])
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME 'and' VARIABLE_LIST", lambda vn, vl: [vn]+vl)
sem.add_rule("VARIABLE_NAME -> Var VARIABLE_NAME", lambda x, v: v)

sem.add_rule("Var -> Det VARS", lambda det, var: var)
sem.add_rule("Var -> VARS", identity)
sem.add_rule("Lis -> Det LISS", lambda det, liss: liss)
sem.add_rule("Lis -> LISS", identity)
sem.add_rule("KEY_NAME -> Det KEY_NAME 'key'", lambda det, name, key: name)
sem.add_rule("KEY_NAME -> KEY_NAME 'key'", lambda name, key: name)
sem.add_rule("KEY_NAME -> Det KEY_NAME", lambda det, name: name)
sem.add_rule("ITEM -> NP", lambda i:i)
sem.add_rule("ITEM -> MESSAGE_NAME", lambda name: name)
sem.add_rule("ITEM -> Unk", lambda name: name)


# Duration
sem.add_rule("Duration -> Unk 'times'", lambda np, times: Dur(times))

# Sound Command 
sem.add_rule("SoundCommand -> 'play' 'the' NAME_OF_SOUND 'sound'", lambda play, the, name, sound: singleCommand("playSound:", name))

sem.add_rule("SoundCommand -> 'set' 'volume' 'to' Unk", lambda sett, volume, too, unk: singleCommand("setVolumeTo:", unk))

sem.add_rule("SoundCommand -> 'set' 'volume' 'to' Unk 'percent'", lambda sett, volume, too, unk, percent: singleCommand("setVolumeTo:", unk))

sem.add_rule("SoundCommand -> 'change' 'volume' 'by' Unk", lambda change, volume, by, Unk: singleCommand("changeVolumeBy:", Unk))

sem.add_rule("SoundCommand -> 'stop' 'all' 'sounds'", lambda stop, all, sounds: singleCommandNoValue("stopAllSounds"))

sem.add_rule("SoundCommand -> 'stop'", lambda stop: singleCommandNoValue("stopAllSounds"))

sem.add_rule("SoundCommand -> 'change' 'pitch' 'effect' 'by' Unk", lambda change, pitch, effect, by, Unk: singleCommand("changeTempoBy:", Unk))

sem.add_rule("SoundCommand -> 'softer'", lambda softer: singleCommand("changeVolumeBy:", -10))

sem.add_rule("SoundCommand -> 'louder'", lambda louder: singleCommand("changeVolumeBy:", 10))

sem.add_rule("SoundCommand -> 'slower'", lambda slower: singleCommand("changeTempoBy:", -10))

sem.add_rule("SoundCommand -> 'faster'", lambda faster: singleCommand("changeTempoBy:", 10))


# Data Command 
sem.add_rule("DataCommand -> 'delete' Var VARIABLE_NAME", lambda delete, var, var_name: deleteVariable(var_name))

sem.add_rule("DataCommand -> 'set' VARIABLE_NAME 'to' BP", lambda s, var_name, to, bp: setVariable(var_name, bp))

sem.add_rule("DataCommand -> 'set' VARIABLE_NAME 'to' Unk", lambda s, var_name, to, unk: setVariable(var_name, unk))
sem.add_rule("DataCommand -> 'add' Unk 'to' VARIABLE_NAME", lambda a, num, t, var_name:
changeVarBy(var_name, num))
sem.add_rule("DataCommand -> 'increment' VARIABLE_NAME 'by' Unk", lambda i, var_name, b, unk: changeVarBy(var_name, num))
# Increment variable 2 by the value in variable 1
sem.add_rule("DataCommand -> 'add' VARIABLE_NAME 'to' VARIABLE_NAME", lambda i, var1, b, var2: changeVarByVar(var2, var1))
sem.add_rule("DataCommand -> 'subtract' Unk 'from' VARIABLE_NAME", lambda a, unk, t, var_name: changeVarBy(var_name, unk, 'negate'))
sem.add_rule("DataCommand -> 'decrement' VARIABLE_NAME 'by' Unk", lambda a, unk, t, var_name: changeVarBy(var_name, unk, 'negate'))
sem.add_rule("DataCommand -> 'subtract' VARIABLE_NAME 'from' VARIABLE_NAME", lambda a, var1, t, var2: changeVarByVar(var2, var1, 'negate'))
sem.add_rule("DataCommand -> 'multiply' VARIABLE_NAME 'by' Unk", lambda m, var_name, unk: setVariable(var_name, getProduct(getValue(var_name), unk)))
# var1 = var1*var2
sem.add_rule("DataCommand -> 'multiply' VARIABLE_NAME 'by' VARIABLE_NAME", lambda m, var1, b, var2: setVariable(var1, getProduct(getValue(var1), getValue(var2))))
sem.add_rule("DataCommand -> 'divide' VARIABLE_NAME 'by' Unk", lambda d, var_name, b, unk: setVariable(var_name, getQuotient(getValue(var_name), unk)))
sem.add_rule("DataCommand -> 'divide' VARIABLE_NAME 'by' VARIABLE_NAME", lambda d, var1, b, var2: setVariable(var1, getQuotient(getValue(var1), getValue(var1))))

sem.add_rule("DataCommand -> 'add' ITEM 'to' Lis LIST_NAME", lambda a, item, t, list_name: appendToList(list_name, item))
sem.add_rule("DataCommand -> 'delete' Ele NP 'of' Lis LIST_NAME", lambda d, el, ind,o, l, list_name: deleteFromList(ind, list_name))
sem.add_rule("DataCommand -> 'replace' Ele NP 'of' Lis LIST_NAME 'with' ITEM", lambda r, e, ind, o,l,list_name,w, item: setItemInList(ind, list_name, item))
sem.add_rule("DataCommand -> 'set' Ele NP 'of' Lis LIST_NAME 'to' ITEM", lambda s, e, ind, o,l, list_name, t,
item: setItemInList(ind, list_name, item))

# Data Reporter
sem.add_rule("DataReporter -> 'the' OrderAdverb 'item' 'in' Lis LIST_NAME", lambda t, order_adverb, i, inn, l, list_name: getItem(mapWordToNum(order_adverb), list_name))

# Number Phrase
sem.add_rule("Unk -> NP", identity)
sem.add_rule("NP -> NPP", identity)
sem.add_rule("NP -> Det NPP", lambda det, npp: npp)
sem.add_rule("NP -> VARIABLE_NAME", identity)
sem.add_rule("NP -> Unk 'plus' Unk", lambda unk1, plus, unk2: add(unk1, unk2)) 
sem.add_rule("NP -> Unk 'added' 'to' Unk", lambda unk1, added, to, unk2: add(unk1, unk2))
sem.add_rule("NPP -> 'sum' 'of' Unk 'and' Unk", lambda s, of, unk1, a,  unk2: add(unk1, unk2))

sem.add_rule("NP -> Unk 'minus' Unk", lambda unk1, minus, unk2: unk1-unk2)
sem.add_rule("NP -> Unk 'subtracted' 'by' Unk", lambda unk1, subtracted, by, unk2: subtract(unk1,unk2))

sem.add_rule("NP -> Unk 'times' Unk", lambda unk1, times, unk2: getProduct(unk1,unk2))
sem.add_rule("NP -> Unk 'multiplied' 'by' Unk", lambda unk1, multiplied, by, unk2: getProduct(unk1,unk2))
sem.add_rule("NPP -> 'product' 'of' Unk 'and' Unk", lambda product, of, unk1, a, unk2: getProduct(unk1,unk2))

sem.add_rule("NP -> Unk 'divided' 'by' Unk", lambda unk1, divided, by, unk2: getQuotient(unk1,unk2))
sem.add_rule("NPP -> 'random' 'number' 'between' Unk 'and' Unk", lambda r, n, b, unk1, a, unk2: getRandomNumberBetween(unk1, unk2))
sem.add_rule("NP -> 'negative' NP", lambda n, np: getProduct(-1,np))
sem.add_rule("NP -> 'negative' Unk", lambda n, unk: getProduct(-1,unk))

sem.add_rule("EVENT -> 'when' 'the' 'green' 'flag' 'is' 'clicked'", lambda w, t, g, f, i, c: whenGreenFlag())
sem.add_rule("EVENT -> 'when' 'the' 'program' 'starts'", lambda w, t, p, s: whenGreenFlag())
sem.add_rule("EVENT -> 'when' KEY_NAME 'is' 'pressed'", lambda w, name, iss, pressed: whenKeyPress(name))
sem.add_rule("EVENT -> 'when' 'this' 'sprite' 'is' 'clicked'", lambda w, t, iss, cli: whenClicked())
sem.add_rule("EVENT -> 'when' 'backdrop' 'switches' 'to' BACKDROP_NAME", lambda w, b, s, t, name: whenBackSwitch(name))
sem.add_rule("EVENT -> 'when' 'backdrop' 'switches' 'to' 'the' BACKDROP_NAME", lambda w, b, s, t, th, name: whenBackSwitch(name))
sem.add_rule("EVENT -> 'when' 'I' 'receive' MESSAGE_NAME", lambda w, i, r, message: whenReceive(message))

sem.add_rule("Tim -> Det 'timer'", lambda d, tim: ["timer"])

sem.add_rule("'when' Tim CBP Unk", lambda w, tim, comp, Unk: comp(tim, Unk)) ## RIGHT WAY TO CALL?

sem.add_rule("'equal' 'to'", lambda e, t: lambda a, b: equalTo(a,b))
sem.add_rule("'greater' 'than'", lambda g, t: lambda a, b: greaterThan(a, b))
sem.add_rule("'less' 'than'", lambda l, t: lambda a, b: lessThan(a, b))
sem.add_rule("'greater' 'than' 'or' 'equal' 'to'", lambda l, t: lambda a, b: GEQ(a, b))
sem.add_rule("'less' 'than' 'or' 'equal' 'to'", lambda l, t: lambda a, b: LEQ(a, b))
sem.add_rule("'when' Tim CBP Unk", lambda w, t, c, n: waitTillTimer(c(["timer"], n)))
sem.add_rule("CBP -> LMOD CBP", lambda m, c: m(c))

sem.add_rule("LMOD -> POS", identity)
sem.add_rule("LMOD -> NEG", identity)
sem.add_rule("POS ->'is'", lambda word: None)
sem.add_rule("NEG -> 'is' 'not'", lambda iss, word: lambda x: not_identity(x))
sem.add_rule("NEG -> 'not'", lambda word: lambda x: not_identity(x))
sem.add_rule("NEG -> 'isn't'", lambda word: lambda x: not_identity(x))


## Event Handler
sem.add_rule("SimpleEventHandler -> EVENT AL", lambda e, a: SimpleEvent(e, a))
sem.add_rule("EventHandler ->  SimpleEventHandler", identity)
sem.add_rule("EventHandler -> SimpleEventHandler 'at' 'the' 'same' 'time'", lambda e, a, t, s, ti: e)
sem.add_rule("EventHandler -> SimpleEventHandler 'too'", lambda e, t: e)
sem.add_rule("EventHandler -> SimpleEventHandler 'simultaneously'", lambda e, s: e)
sem.add_rule("EventHandler -> SimpleEventHandler 'at' 'the' 'same' 'time' 'too'", lambda e, a, t, s, ti, to: e)

## TimerCommand 
sem.add_rule("TimerCommand -> 'reset' Tim", lambda r, t: resetTimer())
sem.add_rule("Ele -> 'element'", identity)
sem.add_rule("Ele -> Det 'element'", lambda d, e: e)

## Boolean Phrases
sem.add_rule("BP -> 'item' Unk 'in' Lis LIST_NAME", lambda i, unk, inn, liss, name: itemInList(unk, name))
sem.add_rule("BP -> 'item' Unk MOD 'in' Lis LIST_NAME", lambda i, unk, mod, inn, liss, name: mod(itemInList(unk, name)))
sem.add_rule("BP -> VARIABLE_NAME CBP Unk", lambda var, cbp, unk: cbp(getValue(var), unk))
sem.add_rule("BP -> VARIABLE_NAME MOD CBP Unk", lambda var, mod, cbp, unk: mod(cbp(getValue(var), unk)))
sem.add_rule("BP -> Unk CBP Unk", lambda unk1, cbp, unk2: cbp(unk1, unk2))
sem.add_rule("BP -> VARIABLE_NAME CBP VARIABLE_NAME", lambda var1, cbp, var2: cbp(getValue(var1), getValue(var2)))
sem.add_rule("BP -> Tim CBP Unk", lambda tim, cbp, Unk: cbp(["timer"],unk))
sem.add_rule("BP -> LIST_NAME 'contains' ITEM", lambda name, con, it: itemInList(it, name))
sem.add_rule("BP -> Boolean" , identity)
sem.add_rule("Boolean -> 'true'" , lambda t: 1)
sem.add_rule("Boolean -> 'false'" , lambda t: 0)
sem.add_rule("Boolean -> LMOD 'true' ", lambda l, t: l(1))
sem.add_rule("Boolean -> LMOD 'false'" , lambda l, t: l(0))
sem.add_rule("BP -> BP 'and' BP", lambda b1,andd, bp: logicAnd(b1, b2))
sem.add_rule("BP -> BP 'or' BP", lambda b1, orr, b2: logicOr(b1, b2))

## Broadcast Commands
sem.add_rule("BroadcastCommand -> 'broadcast' MESSAGE_NAME", lambda broadcast, name: broadcastMessage(name))
sem.add_rule("BroadcastCommand -> 'broadcast' MESSAGE_NAME 'and' 'wait'", lambda b, name, a, w: broadCastMessageWait(name))
sem.add_rule("BroadcastCommand -> 'broadcast' 'a' 'new' 'message' 'called' MESSAGE_NAME", lambda b, a, n, m, c, name: broadcastMessage(name))


## ConditionalCommands
sem.add_rule("ConditionalCommand -> 'if' BP 'then' AL Thatsit", lambda i, bp, then, al, thatsit: ifCommand(bp,al))

sem.add_rule("ConditionalCommand -> 'if' BP 'then' AL Thatsit otherwise AL Thatsit", lambda i, bp, then, al1, thatsit, ow, al2, thatsit2: ifElseCommand(bp,al1,al2))

sem.add_rule("ConditionalCommand -> 'if' BP 'then' AL Thatsit else AL Thatsit", lambda i, bp, then, al1, thatsit, ow, al2, thatsit2: ifElseCommand(bp,al1,al2))

sem.add_rule("ControlCommand -> 'wait' Unk 'seconds'", lambda wait, unk, seconds: wait(unk))

sem.add_rule("ControlCommand -> 'wait' 'until' BP", lambda wait, until, bp: waitUntil(bp))

sem.add_rule("ControlCommand -> 'repeat' AL 'until' BP", lambda repeat, al, until, bp: until(bp, al))

sem.add_rule("ControlCommand -> 'repeat' AL 'forever'", lambda repeat, al, forever: doForever(al))

sem.add_rule("ControlCommand -> 'repeat' AL Unk 'times'", lambda repeat, al, unk, times: repeat(unk, al))

sem.add_rule("ControlCommand -> 'delete' 'this' 'clone'", lambda delete, this, clone: deleteClone())


#LoopCommand
sem.add_rule("LoopCommand -> 'repeat' LoopCommandP", lambda r, lcp: lcp)
sem.add_rule("LoopCommand -> LoopCommandP", identity)
sem.add_rule("LoopCommand -> AL 'that' 'should' 'be' 'repeated' Duration", lambda action_list, t,s,b,r, duration: repeat_action_list(action_list, duration))
#sem.add_rule("LoopCommand -> AL 'repeat' 'that' Duration", lambda action_list, r, t, duration: repeat_action_list(action_list, duration))
#sem.add_rule("LoopCommand -> AL 'repeat' 'this' Duration", lambda action_list, r, t, duration: repeat_action_list(action_list, duration))

sem.add_rule("LoopCommandP -> AP Duration", lambda ap, duration: repeat_action_list([ap], duration))
sem.add_rule("LoopCommandP -> 'the' 'following' Duration AL Thatsit", lambda t, f, duration, action_list, tt: repeat_action_list(action_list, duration))
sem.add_rule("LoopCommandP -> 'the' 'following' 'steps' Duration AL Thatsit", lambda t, f, s, duration, action_list, tt: repeat_action_list(action_list, duration))


#####################################################################
## Lexicon

# Names
sem.add_lexicon_rule("NAME_OF_SOUND",
                     ['meow'],
                     lambda name: name)

# # Common nouns
# sem.add_lexicon_rule("N[-mass, number=singular]",
#                      ['book', 'city', 'dog', 'man', 'park', 'woman', 'country'],
#                      lambda word: lambda det, apstar:\
#                          C("Object", type=word, definite=det, mod=apstar))


# # Determiners
sem.add_lexicon_rule("Det",
                      ['the', 'this'],
                      lambda word: lambda: None)

sem.add_lexicon_rule("Det",
                      ['a', 'an'],
                      lambda word: lambda: None)
 
sem.add_lexicon_rule("VARS",
                      ['variable', 'variable' 'called'],
                      lambda word: word)

sem.add_lexicon_rule("LISS",
                      ['list', 'list' 'called'],
                      lambda word: word)

sem.add_lexicon_rule("Tim",
                      ['timer'],
                      ["timer"])
                      
sem.add_lexicon_rule("OrderAdverb",
                       ['secondly', 'fourthly', 'fifthly', 'seventh', 'second', 'fifth', 'sixthly', 'third', 'thirdly', 'fourth', 'sixth', 'firstly', 'first'],
                       lambda word: wordMap(word))
   
# handle sequencing adverbs                    
sem.add_lexicon_rule("SequenceAdverb",
                       ['then', 'after', 'finally'],
                       identity)
                       
sem.add_lexicon_rule("Duration",
                       ['forever'],
                       lambda word: Dur(-1))
                       
sem.add_lexicon_rule("Unk",
                       ['0','1','2','3','4','5','6','7','8','9'],
                       identity)    
                       


        
                     
##############################################################################
# Now we will run the rules you are adding to solve problems in this lab.
import my_rules
my_rules.add_my_rules(sem)


