# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'../software/')
import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry

from nltk.corpus import wordnet as wn
from text2num import text2float

sys.path.insert(0,'../server/flaskr')
import random
from sounds import get_sounds

############################synonym helpers #########################
def getWordsInSynset(synset):
	words = set()
	lemmas = synset.lemmas()
	for lemma in lemmas:
		this_synonym = str(lemma.name())
		words.add(this_synonym)
	return words
def findSynonyms(word, part_of_speech):
	synonyms = set()
	synsets_found = wn.synsets(word, part_of_speech)
	for synset in synsets_found:
		current_synset_synonyms = getWordsInSynset(synset)
		synonyms.update(current_synset_synonyms)
	#convert to array form to be added in semanticRules
	synonyms = list(synonyms)
	return synonyms
####################################################################

def translate(data):
	pass

def translateModifier(data):
	pass

####################################################################

identity = lambda x: x

sem = SemanticRuleSet()
global_variables = {}
global_lists = {}
global_sounds = set()

####################################################################
# Music Actions
def soundToNumber(string):

	sounds = {"snare drum": 1, "base drum": 2, "side stick": 3, "crash cymbal": 4, "open hi hat": 5, "open highhat": 5, "closed hi hat": 6, "closed highhat": 6, "tambourine": 7, "hand clap": 8, "claves": 9, "wood block": 10, "cowbell": 11, "triangle": 12, "bongo": 13, "conga": 14, "cabasa": 15, "guiro": 16, "vibraslap": 17, "cuica": 18}
	if string in sounds:
		return sounds[string]
	else:
		## TODO RAISE ERROR
		return 1

def playInstrumentBeats(sound, beats):
	return ["playDrum", sound, beats]

def InstrumentToNumber(string):
	sounds = {"piano": 1, "electric piano": 2, "organ": 3, "guitar": 4, "electric guitar": 5, "bass": 6, "pizzicato": 7, "cello": 8, "trombone": 9, "clarinet": 10, "saxophone": 11, "flute": 12, "wooden flute": 13, "bassoon": 14, "choir": 15, "vibraphone": 16, "music box": 17, "steel drum": 18, "marimba": 18, "synth lead": 20, "synth pad": 21}
	if string in sounds:
		return sounds[string]
	else:
		## TODO RAISE ERROR
		return 0

def playInstrumentBeats(sound, beats):
    # Add the sound to the project.
    global_sounds.add(string.title())
    return ["playDrum", sound, beats]

def setInstrument(num):
	return ["instrument:", num]

def playNoteDuration(note, duration):
	return ["noteOn:duration:elapsed:from:", note, duration]

def setTempo(num):
	return ["setTempoTo:", num]

def changeTempo(num):
	return ["changeTempoBy:", num]

# Speech Actions
def processSentence(data):
	if len(data) > 0:
		data = [thing for thing in data if thing != None]
		return {'scripts': data, 'variables': global_variables, 'lists': global_lists, 'sounds': global_sounds}

def processPartial(data):
	# print(data)
	return {'scripts': [], 'variables': global_variables, 'lists': global_lists, "incomplete": data, 'sounds': global_sounds}

def singleCommand(commandName, value):
	return [commandName, value]

def singleCommandNoValue(commandName):
	return [commandName]

def playSound(name):
    # Add the sound to the project.
    global_sounds.add(name.title())
    return ["doPlaySoundAndWait", name.title()]

def ifCommand(if_cond, if_body):
	return ["doIf", if_cond, if_body]

def ifElseCommand(if_cond, if_body, else_body):
	return ["doIfElse", if_cond, if_body, else_body]


def repeat(num_times, repeat_body):
	return ["doRepeat", int(num_times), [repeat_body]]
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

def getNumber(unk):
		try:
			num = int(unk)
		except:
			# num = text2int(unk)
			num = text2float(unk)
		return num

def setVariable(var_name, value):
	#global_variables[var_name] = value
	return ["setVar:to:",var_name, value]

def deleteVariable(variable_name):
	del global_variables[variable_name]
	return wait(0.1)

def createVariable(variable_list):
	for var in variable_list:
		global_variables[var] = 0
	return wait(0.1)
		# TODO: somehow prevent returning the variable name in response of processSentence.
	#return None

def createSingleList(name):
	global_lists[name] = []
	return wait(0.1)


def createClone():
	return ["createCloneOf:", "myself"]

def itemInList(unk, name):
	return ["list:contains:", name, unk]

def resetTimer():
	return ["timerReset"]

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
	return ["readVariable", var]

def getRandomNumberBetween(unk1, unk2):
	return ['randomFrom:to:', unk1, unk2]

def getRandomSound():
    sound = random.choice(get_sounds())
    return sound["soundName"]

def lessThan(a,b):
	return ["<", a, b]

def greaterThan(a,b):
	return [">", a, b]

def equalTo(a,b):
	return ["=", a, b]

def GEQ(a,b):
	return ["|", [">", a, b], ["=", a, b]]

def LEQ(a,b):
	return ["|", ["<", a, b], ["=", a, b]]

def logicOr(b1, b2):
	return ["|", b1, b2]

def logicAnd(b1, b2):
	return ["&", b1, b2]

def waitTillTimer(x):
	return ["doWaitUntil", x]

def negate(unk):
	return ["*", unk, -1]

def changeVarBy(var_name, unk, opt_negate=False):
	if opt_negate:
		return ["changeVar:by:", var_name, ["*", unk, -1]]
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

def whenYouHear(word_phrase):
	return ["whenIHear", word_phrase]

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
	# flatten the action list
	return [e] + a

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
	return ['append:toList:', item, list_name]

def deleteListItem(list_name, ind):
	return ['deleteLine:ofList:', ind, list_name]

def setItemInList(ind, list_name, item):
	return ['setLine:ofList:to:', ind, list_name, item]

# Loop commands
def repeat_action_list(action_list, duration):
	if duration == 'forever':
		return ['doForever', action_list]
	else:
		return ['doRepeat', duration, action_list]

def get_duration(duration):
		return duration

# Sequential commands
def appendToProgram(action_list):
	program.append(action_list)
	return action_list

def incompleteCommand(t, end, cur):
	'''
	Return a dictionary with the following information:

	Type: Type of incomplete command, could be "conditional", "event", "loop"
	End Keyword: List of possible keywords to indicate the completed instruction
	Current Parse: The current parse 
	'''

	return {"type": t, "end keyword": end, "current parse": cur}


def getAP(phrase):
    def isMultiCommand(phrase):
        # Some commands are actually a list of multiple commands that must be
        # on the same level as other commands.
        # e.g. "if i say" or "if you hear" Conditional Command)
        return len(phrase) == 2 and  phrase[0][0] == "listenAndWait" and phrase[1][0] == "doIf"

    if isMultiCommand(phrase):
        # MultiCommandsalready have an encapsulating set of brackets.
        return phrase
    else:
        return [phrase]

####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))
sem.add_rule("Start -> IC", lambda ic: processPartial(ic))

# All Command
sem.add_rule("S -> AL", identity)
sem.add_rule("S -> PRE AL", lambda p, a: a)
sem.add_rule("AL -> AP", lambda p: getAP(p))
sem.add_rule("AL -> AP AL", lambda p, l: [p]+l)
sem.add_rule("AL -> AP And AL", lambda p,an, l: [p]+l)

sem.add_rule("AP -> Text2SpeechCommand", identity)
sem.add_rule("AP -> Speech2TextCommand", identity)
sem.add_rule("AP -> MusicCommand", identity)
sem.add_rule("AP -> SoundCommand", identity)
sem.add_rule("AP -> CreateCommand", identity)
sem.add_rule("AP -> DataCommand", identity)
sem.add_rule("AP -> EventHandler", identity)
# sem.add_rule("AP -> EventHandler", lambda eventHandler: [111,124, eventHandler])
#sem.add_rule("AP -> SequentialCommand", identity)
sem.add_rule("AP -> ConditionalCommand", identity)
sem.add_rule("AP -> LoopCommand", identity)
sem.add_rule("AP -> TimerCommand", identity)
sem.add_rule("AP -> BroadcastCommand", identity)
sem.add_rule("AP -> ControlCommand", identity)
sem.add_rule("AL -> SequentialCommand", identity)
sem.add_rule("AL -> OrderedCommand", identity)

sem.add_rule("PRE -> Can You", lambda c, y: c)
sem.add_rule("PRE -> Can I", lambda c, y: c)
sem.add_rule("PRE -> Please", lambda c: c)

# Ordered Command
sem.add_rule("OrderedCommand -> OrderAdverb AL", lambda num, al: al)

# SequentialCommand
sem.add_rule("SequentialCommand -> SequenceAdverb AL", lambda seq_adv, action_list: action_list)

# Create Command
sem.add_rule("CreateCommand -> Make Det Clone Of Myself", lambda m, det, c,o, my: createClone())
sem.add_rule("CreateCommand -> Make VARIABLE_LIST", lambda make, vl: createVariable(vl))
sem.add_rule("CreateCommand -> Make LIST_NAME", lambda make, name: createSingleList(name))

# Variable Handling
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME", lambda vl: [vl])
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME And VARIABLE_LIST", lambda vn, a, vl: [vn]+vl)
sem.add_rule("VARIABLE_NAME -> Variable VARIABLE_NAME", lambda l, name: name)
sem.add_rule("Variable -> Det Variable", lambda det, var: None)
sem.add_rule("Variable -> Your Variable", lambda det, var: None)
sem.add_rule("Variable -> My Variable", lambda det, var: None)
sem.add_rule("Variable -> Variable Called", lambda v, c: None)
sem.add_rule("Variable -> New Variable", lambda v, c: None)

# List Handling
sem.add_rule("LIST_NAME -> List LIST_NAME", lambda l, name: name)
sem.add_rule("List -> Det List", lambda det, liss: None)
sem.add_rule("List -> Your List", lambda det, liss: None)
sem.add_rule("List -> My List", lambda det, liss: None)
sem.add_rule("List -> New List", lambda det, liss: None)
sem.add_rule("List -> List Called", lambda liss, c: None)

sem.add_rule("KEY_NAME -> KEY_NAME Key", lambda name, key: name)
sem.add_rule("KEY_NAME -> Det KEY_NAME", lambda det, name: name)
sem.add_rule("KEY_NAME -> Direction Key", lambda name, key: name+" arrow")

sem.add_rule("ITEM -> NP", lambda i:i)
sem.add_rule("ITEM -> MESSAGE_NAME", lambda name: name)
sem.add_rule("ITEM -> BP", lambda name: name)
#sem.add_rule("ITEM -> VARIABLE_NAME", lambda name: name)
sem.add_rule("ITEM -> DATA_REPORTER", identity)

sem.add_rule("ITEM -> WP", lambda i:i) # Word phrase

sem.add_rule("WP -> WP_1", lambda i:i) # Speech phrase
sem.add_rule("WP -> WP_2", lambda i:i) # Speech phrase
sem.add_rule("WP_1 -> SP", lambda i:i) # Speech phrase
sem.add_rule("WP_2 -> Word", lambda unk:unk) # Word phrase can map to what someone said.
sem.add_rule("WP_2 -> Word WP_2", lambda w1, wp : ' '.join([w1, wp])) # Word phrase can map to what someone said.

# Duration
sem.add_rule("Duration -> NP Times", lambda np, times: get_duration(np))

# Speech2Text Commands
sem.add_rule("Speech2TextCommand -> Listen And Wait", lambda l, a, w: singleCommandNoValue("listenAndWait"))
sem.add_rule("Speech2TextCommand -> Wait For Det Response", lambda w, f, d, r: singleCommandNoValue("listenAndWait"))
sem.add_rule("Speech2TextCommand -> Wait For Det Response", lambda w, f, d, r: singleCommandNoValue("listenAndWait"))
sem.add_rule("SP -> Det Speech", lambda t, speech: singleCommandNoValue("getSpeech"))
# sem.add_rule("EVENT -> When You Hear WP", lambda w, y, hear, wp: whenYouHear(wp))
# sem.add_rule("EVENT -> When I Say WP", lambda w, y, hear, wp: whenYouHear(wp))
sem.add_rule("EVENT -> Every Time You Hear WP", lambda e, t, y, hear, wp: whenYouHear(wp))
sem.add_rule("EVENT -> Every Time I Say WP", lambda e, t, i, say, wp: whenYouHear(wp))
sem.add_rule("EVENT -> Whenever You Hear WP", lambda we, y, hear, wp: whenYouHear(wp))
sem.add_rule("EVENT -> Whenever I Say WP", lambda we, i, say, wp: whenYouHear(wp))

# Text2Speech Commands
sem.add_rule("Voice -> Det Voice", lambda d, v: v)
sem.add_rule("Voice -> Your Voice", lambda d, v: v)
sem.add_rule("Voice -> My Voice", lambda d, v: v)
sem.add_rule("VOICE_NAME -> Your VOICE_NAME Voice", lambda y, voice_name, v: voice_name)
sem.add_rule("VOICE_NAME -> Det VOICE_NAME Voice", lambda d, voice_name, v: voice_name)
sem.add_rule("VOICE_NAME -> VOICE_NAME Voice", lambda voice_name, v: voice_name)
sem.add_rule("VOICE_NAME -> Voice Called VOICE_NAME", lambda v, c, voice_name: voice_name)
sem.add_rule("VOICE_NAME -> Voice Of VOICE_NAME", lambda v, c, voice_name: voice_name)

sem.add_rule("Text2SpeechCommand -> Say The Speech", lambda s, t, speech: singleCommand("speakAndWait:", singleCommandNoValue("getSpeech")))
sem.add_rule("Text2SpeechCommand -> Say WP", lambda s, wp: singleCommand("speakAndWait:", wp))
sem.add_rule("Text2SpeechCommand -> Set Voice To VOICE_NAME", lambda s, v, t, voice_name: singleCommand("setVoice:", voice_name))
sem.add_rule("Text2SpeechCommand -> Change Voice To VOICE_NAME", lambda c, v, t, voice_name: singleCommand("setVoice:", voice_name))
sem.add_rule("Text2SpeechCommand -> Use VOICE_NAME", lambda u, voice_name: singleCommand("setVoice:", voice_name))
sem.add_rule("Text2SpeechCommand -> Switch Voice To VOICE_NAME", lambda s, v, t, voice_name: singleCommand("setVoice:", voice_name))

sem.add_rule("AccentP -> Det Accent", lambda d, acc: acc)
sem.add_rule("AccentP -> Accent", lambda acc: acc)
sem.add_rule("AccentP -> Your Accent", lambda y, acc: acc)
sem.add_rule("AccentP -> My Accent", lambda y, acc: acc)
sem.add_rule("LANGUAGE_NAMEP -> Accent Called LANGUAGE_NAME", lambda a, c, acc: acc)
sem.add_rule("LANGUAGE_NAMEP -> Accent For LANGUAGE_NAME", lambda a, f, acc: acc)
sem.add_rule("LANGUAGE_NAMEP -> Accent Of LANGUAGE_NAME", lambda a, f, acc: acc)
sem.add_rule("LANGUAGE_NAMEP -> LANGUAGE_NAME", lambda acc: acc)

sem.add_rule("Text2SpeechCommand -> Set AccentP To LANGUAGE_NAMEP", lambda s, l, t, language: singleCommand("setLanguage:", language))
sem.add_rule("Text2SpeechCommand -> Talk With Det LANGUAGE_NAME Accent", lambda t, w, d, language, ac: singleCommand("setLanguage:", language))
sem.add_rule("Text2SpeechCommand -> Change AccentP To LANGUAGE_NAMEP", lambda c, acc, t, language: singleCommand("setLanguage:", language))
sem.add_rule("Text2SpeechCommand -> Use Det LANGUAGE_NAME Accent", lambda u, d, language, a: singleCommand("setLanguage:", language))
sem.add_rule("Text2SpeechCommand -> Switch AccentP To LANGUAGE_NAMEP", lambda s, a, t, language: singleCommand("setLanguage:", language))

# Music Command
sem.add_rule('DRUM -> Drum1 Drum2', lambda i, i2: i + ' ' + i2)
sem.add_rule('DRUM -> Drum1 Drum2 Drum3', lambda i, i2, i3: i + ' ' + i2 + ' ' + i3)
sem.add_rule('DRUM -> DRUM Drum', lambda i, d: i)
sem.add_rule('DRUM -> Drum DRUM', lambda d, i: i)
sem.add_rule('DRUM -> Det DRUM', lambda d, i: i)

sem.add_rule('INSTRUMENT -> Instrument1 Instrument2', lambda i, i2: i + ' ' + i2)
sem.add_rule('INSTRUMENT -> Det INSTRUMENT', lambda d, i: i)
sem.add_rule('Note -> Det Note', lambda d, i: i)

sem.add_rule('MusicCommand -> Use INSTRUMENT', lambda u, i: setInstrument(InstrumentToNumber(i)))
sem.add_rule('MusicCommand -> Set Det Instrument To INSTRUMENT', lambda s, d, i, t, ii: setInstrument(InstrumentToNumber(ii)))
sem.add_rule('MusicCommand -> Use INSTRUMENT As Det Instrument', lambda u, ii, a, d, i: setInstrument(InstrumentToNumber(ii)))
sem.add_rule('MusicCommand -> Play INSTRUMENT', lambda p, i: setInstrument(InstrumentToNumber(i)))
sem.add_rule('MusicCommand -> Play Note NP For NP Beats ', lambda p, n, note, f, beats, b: playNoteDuration(note, beats))

sem.add_rule('Tempo -> Det Tempo', lambda d, t: t)
sem.add_rule('MusicCommand -> Set Tempo To NP ', lambda s, tempo, t, n: setTempo(n))
sem.add_rule('MusicCommand -> Change Tempo By NP ', lambda s, tempo, t, n: changeTempo(n))
sem.add_rule('MusicCommand -> Increment Tempo By NP ', lambda i, tempo, t, n: changeTempo(n))
sem.add_rule('MusicCommand -> Decrement Tempo By NP ', lambda d, tempo, t, n: changeTempo(negate(n)))

sem.add_rule('MusicCommand -> Play DRUM For NP Beats' , lambda p, i, f, n, b: playInstrumentBeats(soundToNumber(i), n))
sem.add_rule('MusicCommand -> Play DRUM NP Beats' , lambda p, i, n, b: playInstrumentBeats(soundToNumber(i), n))
sem.add_rule('MusicCommand -> Use DRUM' , lambda u, i: playInstrumentBeats(soundToNumber(i), n))



# Sound Command
# Use the halting version f the play sound block
sem.add_rule("SoundCommand -> Play NAME_OF_SOUND", lambda play, name: playSound(name))

sem.add_rule("NAME_OF_SOUND -> Det NAME_OF_SOUND", lambda d, name: name.title())
sem.add_rule("NAME_OF_SOUND -> Your NAME_OF_SOUND", lambda d, name: name.title())
sem.add_rule("NAME_OF_SOUND -> NAME_OF_SOUND Sound", lambda name, sound: name.title())
sem.add_rule("NAME_OF_SOUND -> Sound Called NAME_OF_SOUND", lambda s, c, name: name.title())
sem.add_rule("NAME_OF_SOUND -> Random Sound", lambda r, s: getRandomSound());

sem.add_rule("SoundCommand -> Set TheVolume To NP", lambda sett, volume, too, unk: singleCommand("setVolumeTo:", unk))
sem.add_rule("SoundCommand -> Set TheVolume To NP Percent", lambda sett, volume, too, unk, percent: singleCommand("setVolumeTo:", unk))

sem.add_rule("SoundCommand -> Change TheVolume By NP", lambda change, volume, by, Unk: singleCommand("changeVolumeBy:", Unk))
sem.add_rule("SoundCommand -> Change TheVolume By NP Percent", lambda change, volume, by, Unk, p: singleCommand("changeVolumeBy:", Unk))
sem.add_rule("SoundCommand -> Increment TheVolume By NP", lambda change, volume, by, Unk: singleCommand("changeVolumeBy:", Unk))

sem.add_rule("SoundCommand -> Decrement TheVolume By NP", lambda change, volume, by, Unk: singleCommand("changeVolumeBy:", negate(Unk)))
sem.add_rule("SoundCommand -> Decrement TheVolume By NP Percent", lambda change, volume, by, Unk, p: singleCommand("changeVolumeBy:", negate(Unk)))

sem.add_rule("SoundCommand -> Change ThePitch Effect By NP", lambda change, pitch, effect, by, Unk: singleCommand("changeTempoBy:", Unk))

sem.add_rule("TheVolume -> The Volume", lambda d, v: v)
sem.add_rule("TheVolume -> Volume", identity)
sem.add_rule("ThePitch -> The Pitch", lambda d, v: v)
sem.add_rule("ThePitch -> Pitch", identity)

sem.add_rule("SoundCommand -> Stop All Sounds", lambda stop, all, sounds: singleCommandNoValue("stopAllSounds"))
sem.add_rule("SoundCommand -> Stop", lambda stop: singleCommandNoValue("stopAllSounds"))
sem.add_rule("SoundCommand -> Softer", lambda softer: singleCommand("changeVolumeBy:", -10))
sem.add_rule("SoundCommand -> Louder", lambda louder: singleCommand("changeVolumeBy:", 10))
sem.add_rule("SoundCommand -> Slower", lambda slower: singleCommand("changeTempoBy:", -10))
sem.add_rule("SoundCommand -> Faster", lambda faster: singleCommand("changeTempoBy:", 10))


## Data Command

# todo: fix
sem.add_rule("DataCommand -> Delete VARIABLE_NAME", lambda delete, var_name: deleteVariable(var_name))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To BP", lambda s, var_name, to, bp: setVariable(var_name, bp))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To NP", lambda s, var_name, to, np: setVariable(var_name, np))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To ITEM", lambda s, var_name, to, item: setVariable(var_name, item))

sem.add_rule("DataCommand -> Add NP To VARIABLE_NAME", lambda a, num, t, var_name:
changeVarBy(var_name, num))
sem.add_rule("DataCommand -> Increment VARIABLE_NAME By NP", lambda i, var_name, b, num: changeVarBy(var_name, num))
sem.add_rule("DataCommand -> Add VARIABLE_NAME To VARIABLE_NAME", lambda i, var1, b, var2: changeVarByVar(var2, getValue(var1)))

sem.add_rule("DataCommand -> Subtract NP From VARIABLE_NAME", lambda a, np, t, var_name: changeVarBy(var_name, np, 'negate'))
sem.add_rule("DataCommand -> Decrement VARIABLE_NAME By NP", lambda a, var_name, t, np: changeVarBy(var_name, np, 'negate'))
sem.add_rule("DataCommand -> Subtract VARIABLE_NAME From VARIABLE_NAME", lambda a, var1, t, var2: changeVarByVar(getValue(var2), var1, 'negate'))

sem.add_rule("DataCommand -> Multiply VARIABLE_NAME By NP", lambda m, var_name, b, np: setVariable(var_name, getProduct(getValue(var_name), np)))
sem.add_rule("DataCommand -> Multiply VARIABLE_NAME By VARIABLE_NAME", lambda m, var1, b, var2: setVariable(var1, getProduct(getValue(var1), getValue(var2))))

sem.add_rule("DataCommand -> Divide VARIABLE_NAME By NP", lambda d, var_name, b, np: setVariable(var_name, getQuotient(getValue(var_name), np)))
sem.add_rule("DataCommand -> Divide VARIABLE_NAME By VARIABLE_NAME", lambda d, var1, b, var2: setVariable(var1, getQuotient(getValue(var1), getValue(var2))))
sem.add_rule("DataCommand -> Change VARIABLE_NAME By NP", lambda c, var1, b, np: changeVarBy(getValue(var1), np))


# todo: fix commands working w/ lists
sem.add_rule("Ele -> Det Ele", lambda d, e: e)
sem.add_rule("DataCommand -> Add ITEM To LIST_NAME", lambda a, item, t, list_name: addToList(list_name, item))
sem.add_rule("DataCommand -> Delete Ele NP Of LIST_NAME", lambda d, el, ind,o, list_name: deleteListItem(list_name,ind))
sem.add_rule("DataCommand -> Replace Ele NP Of LIST_NAME With ITEM", lambda r, e, ind, o, list_name,w, item: setItemInList(ind, list_name, item))
sem.add_rule("DataCommand -> Set Ele NP Of LIST_NAME To ITEM", lambda s, e, ind, o, list_name, t,item: setItemInList(ind, list_name, item))

# Data Reporter
sem.add_rule("DataReporter -> The OrderAdverb Item In LIST_NAME", lambda t, order_adverb, i, inn, list_name: getItem(wordMap(order_adverb), list_name))

# Number Phrase
sem.add_rule("NP -> Unk", lambda unk: getNumber(unk))
sem.add_rule("NP -> NPP", identity)
sem.add_rule("NP -> Det NPP", lambda det, npp: npp)
sem.add_rule("NP -> VARIABLE_NAME", lambda v: getValue(v))

sem.add_rule("NP -> NP Plus NP", lambda unk1, plus, unk2: add(unk1, unk2))
sem.add_rule("NP -> NP Added To NP", lambda unk1, added, to, unk2: add(unk1, unk2))
sem.add_rule("NPP -> Sum Of NP And NP", lambda s, of, unk1, a, unk2: add(unk1, unk2))

sem.add_rule("NP -> NP Minus NP", lambda unk1, minus, unk2: subtract(unk1, unk2))
sem.add_rule("NP -> NP Subtracted By NP", lambda unk1, subtracted, by, unk2: subtract(unk1,unk2))
sem.add_rule("NP -> NP Subtracted From NP", lambda unk1, subtracted, by, unk2: subtract(unk2,unk1))
sem.add_rule("NP -> Difference Between NP And NP", lambda d, b, n1, a, n2: subtract(n1,n2))

sem.add_rule("NP -> NP Times NP", lambda unk1, times, unk2: getProduct(unk1,unk2))
sem.add_rule("NP -> NP Multiplied By NP", lambda unk1, multiplied, by, unk2: getProduct(unk1,unk2))
sem.add_rule("NPP -> Product Of NP And NP", lambda product, of, unk1, a, unk2: getProduct(unk1,unk2))

sem.add_rule("NP -> NP Divided By NP", lambda unk1, divided, by, unk2: getQuotient(unk1,unk2))

sem.add_rule("NPP -> Random Number Between NP And NP", lambda r, n, b, unk1, a, unk2: getRandomNumberBetween(unk1, unk2))
sem.add_rule("NP -> Negative NP", lambda n, np: getProduct(-1,np))

sem.add_rule("Backdrop -> Det Backdrop", lambda d, b: b)
sem.add_rule("Backdrop -> Your Backdrop", lambda d, b: b)
sem.add_rule("Backdrop -> My Backdrop", lambda d, b: b)
sem.add_rule("BACKDROP_NAME -> Det BACKDROP_NAME", lambda d, b: b)
sem.add_rule("BACKDROP_NAME -> Backdrop Called BACKDROP_NAME", lambda d, c, b: b)
sem.add_rule("BACKDROP_NAME -> Backdrop Of BACKDROP_NAME", lambda d, c, b: b)

sem.add_rule("Program -> Det Program", lambda d, p: p)
sem.add_rule("Program -> My Program", lambda d, p: p)
sem.add_rule("Program -> Your Program", lambda d, p: p)

sem.add_rule("Timer -> Det Timer", lambda d, tim: [tim])
sem.add_rule("Timer -> My Timer", lambda d, tim: [tim])
sem.add_rule("Timer -> Your Timer", lambda d, tim: [tim])

sem.add_rule("Sprite -> Det Sprite", lambda d, s: s)
sem.add_rule("Sprite -> My Sprite", lambda d, s: s)
sem.add_rule("Sprite -> Your Sprite", lambda d, s: s)

sem.add_rule("EVENT -> When EVENTDES", lambda w, e: e)
sem.add_rule("EVENTDES -> STARTEVENT", lambda s:s)
sem.add_rule("EVENTDES -> KEYEVENT", lambda s:s)

sem.add_rule("STARTEVENT -> Det Green Flag Is Clicked", lambda t, g, f, i, c: whenGreenFlag())
sem.add_rule("STARTEVENT -> Green Flag Is Clicked", lambda g, f, i, c: whenGreenFlag())
sem.add_rule("STARTEVENT -> Program Starts", lambda p, s: whenGreenFlag())
sem.add_rule("KEYEVENT -> KEY_NAME Is Clicked", lambda name, iss, pressed: whenKeyClicked(name))
sem.add_rule("KEYEVENT -> Direction Is Clicked", lambda name, iss, pressed: whenKeyClicked(name + " arrow"))
sem.add_rule("EVENTDES -> Sprite Is Clicked", lambda s, iss, cli: whenClicked())
sem.add_rule("EVENTDES -> Backdrop Switches To BACKDROP_NAME", lambda w, b, s, t, name: whenBackSwitch(name))
sem.add_rule("EVENTDES -> I Receive MESSAGE_NAME", lambda i, r, message: whenReceive(message))
sem.add_rule("EVENTDES -> Timer CBP NP", lambda t, c, n: waitTillTimer(c([t], n)))

sem.add_rule("CBP -> CBP_equality", lambda i: i)
sem.add_rule("CBP_equality -> Equal To", lambda e, t: lambda a, b: equalTo(a,b))
sem.add_rule("CBP_equality -> Equals", lambda e: lambda a, b: equalTo(a,b))
sem.add_rule("CBP -> Greater Than", lambda g, t: lambda a, b: greaterThan(a, b))
sem.add_rule("CBP -> Less Than", lambda l, t: lambda a, b: lessThan(a, b))
sem.add_rule("CBP -> Greater Than Or Equal To", lambda g, t, o, e, too: lambda a, b: GEQ(a, b))
sem.add_rule("CBP -> Less Than Or Equal To", lambda l, t, o, e, too: lambda a, b: LEQ(a, b))

sem.add_rule("CBP -> LMOD CBP", lambda m, c: lambda a, b: m(c(a, b)))
sem.add_rule("CBP_equality -> LMOD CBP_equality", lambda m, eq: m(eq))

sem.add_rule("LMOD -> POS", lambda pos: lambda x: x)
sem.add_rule("LMOD -> NEG", lambda neg: lambda x: not_identity(x))

sem.add_rule("SimpleEventHandler -> EVENT AL ", lambda e, a: SimpleEvent(e, a))
sem.add_rule("EventHandler ->  SimpleEventHandler Thats It", lambda e, thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Thats It", lambda e, a, t, s, ti, thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler Too Thats It", lambda e, t,thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Too Thats It", lambda e, a, t, s, ti, to, thats, it: e)
sem.add_rule("EventHandler -> AL EVENT", lambda a, e: SimpleEvent(e, a))


sem.add_rule("IC -> When", lambda w: incompleteCommand("event", "thats it", "?"))
sem.add_rule("IC -> EVENT", lambda e: incompleteCommand("event", "thats it", [e, "?"]))
sem.add_rule("IC -> SimpleEventHandler", lambda e: incompleteCommand("event", "thats it", e))
sem.add_rule("IC -> SimpleEventHandler At Det Same Time", lambda e, a, d, s, t: incompleteCommand("event", "thats it", e))
sem.add_rule("IC -> SimpleEventHandler Too", lambda e, t: incompleteCommand("event", "thats it", e))
sem.add_rule("IC -> SimpleEventHandler At Det Same Time Too", lambda e, a, d, s, t, tt: incompleteCommand("event", "thats it", e))

## TimerCommand
sem.add_rule("TimerCommand -> Reset Timer", lambda r, t: resetTimer())

## Boolean Phrases
sem.add_rule("Boolean -> TRUE" , lambda t: lambda x: x)
sem.add_rule("Boolean -> FALSE" , lambda t: lambda x: not_identity(x))
sem.add_rule("Boolean -> LMOD TRUE ", lambda l, t: lambda x: l(x))
sem.add_rule("Boolean -> LMOD FALSE" , lambda l, t: lambda x: l(not_identity(x)))

sem.add_rule("BP -> Ele NP In LIST_NAME", lambda i, unk, inn, name:itemInList(unk, name))
sem.add_rule("BP -> Ele NP LMOD In LIST_NAME", lambda i, unk, mod, inn, name: mod(itemInList(unk, name)))
sem.add_rule("BP -> LIST_NAME Contains ITEM", lambda name, con, it: itemInList(it, name))
#sem.add_rule("BP -> VARIABLE_NAME CBP NP", lambda var, cbp, unk: cbp(getValue(var), unk))
sem.add_rule("BP -> NP CBP NP", lambda unk1, cbp, unk2: cbp(unk1, unk2))
sem.add_rule("BP -> Timer CBP NP", lambda tim, comp, Unk: comp(tim, Unk))
sem.add_rule("BP -> VARIABLE_NAME CBP VARIABLE_NAME", lambda var1, cbp, var2: cbp(getValue(var1), getValue(var2)))

sem.add_rule("BP -> BP Boolean" , lambda b, boo: boo(b))
sem.add_rule("BP -> BP And BP", lambda b1,andd, b2: logicAnd(b1, b2))
sem.add_rule("BP -> BP Or BP", lambda b1, orr, b2: logicOr(b1, b2))
sem.add_rule("BP -> SBP", lambda sbp: sbp)

## Comparison and Logic
sem.add_rule("CBP -> CBP_equality", lambda i: i)
sem.add_rule("CBP_equality -> Equal To", lambda e, t: lambda a, b: equalTo(a,b))
sem.add_rule("CBP_equality -> Equals", lambda e: lambda a, b: equalTo(a,b))
sem.add_rule("CBP -> Greater Than", lambda g, t: lambda a, b: greaterThan(a, b))
sem.add_rule("CBP -> Less Than", lambda l, t: lambda a, b: lessThan(a, b))
sem.add_rule("CBP -> Greater Than Or Equal To", lambda g, t, o, e, too: lambda a, b: GEQ(a, b))
sem.add_rule("CBP -> Less Than Or Equal To", lambda l, t, o, e, too: lambda a, b: LEQ(a, b))

sem.add_rule("CBP -> LMOD CBP", lambda m, c: lambda a, b: m(c(a, b)))
sem.add_rule("CBP_equality -> LMOD CBP_equality", lambda m, eq: m(eq))

sem.add_rule("LMOD -> POS", lambda pos: lambda x: x)
sem.add_rule("LMOD -> NEG", lambda neg: lambda x: not_identity(x))

sem.add_rule("SBP -> SP CBP_equality WP", lambda sp, eq, wp: equalTo(sp,wp)) # SBP = speech boolean phrase
sem.add_rule("SBP -> WP CBP_equality SP", lambda sp, eq, wp: equalTo(sp,wp))

## Broadcast Commands
sem.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME", lambda broadcast, name: broadcastMessage(name))
sem.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME And Wait", lambda b, name, a, w: broadCastMessageWait(name))
sem.add_rule("MESSAGE_NAME -> Det MESSAGE_NAME", lambda d, name: name)
sem.add_rule("MESSAGE_NAME -> Message MESSAGE_NAME", lambda d, name: name)
sem.add_rule("Message -> New Message", lambda d, name: name)
sem.add_rule("Message -> Det Message", lambda d, name: name)
sem.add_rule("Message -> Message Called", lambda d, name: name)

# Conditional Command

# sem.add_rule("ConditionalCommand -> If BP Then AL Thats It", lambda i, bp, then, al, thats, it: ifCommand(bp,al))
# sem.add_rule("ConditionalCommand -> If BP AL Thats It", lambda i, bp, al, thats, it: ifCommand(bp,al))
# sem.add_rule("ConditionalCommand -> If BP Then AL Thats It Else AL Thats It", lambda i, bp, then, al1, thats1, it1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
# sem.add_rule("ConditionalCommand -> If BP AL Thats It Else AL Thats It", lambda i, bp, al1, thats1, it1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
# sem.add_rule("ConditionalCommand -> If BP Then AL Else AL Thats It", lambda i, bp, then, al1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
# sem.add_rule("ConditionalCommand -> If BP AL Else AL Thats It", lambda i, bp, al1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))

sem.add_rule("IfCommand -> If BP Then AL Thats It", lambda i, bp, then, al, thats, it: (bp,al))
sem.add_rule("IfCommand -> If BP AL Thats It", lambda i, bp, al, thats, it: (bp,al))
sem.add_rule("ElseCommand -> Else AL Thats It", lambda e, al, t, i: al)
sem.add_rule("ConditionalCommand -> IfCommand", lambda i: ifCommand(i[0], i[1]))
sem.add_rule("ConditionalCommand -> IfCommand ElseCommand", lambda i, e: ifElseCommand(i[0], i[1], e))

sem.add_rule("IC -> If", lambda i: incompleteCommand("conditional", "thats it", ifCommand("?", "?")))
sem.add_rule("IC -> If BP", lambda i, bp: incompleteCommand("conditional", "thats it", ifCommand(bp, "?")))
sem.add_rule("IC -> If BP AL", lambda i, bp, al: incompleteCommand("conditional", "thats it", ifCommand(bp, al + ["?"])))
sem.add_rule("IC -> If BP Then", lambda i, bp, t: incompleteCommand("conditional", "thats it", ifCommand(bp, "?")))
sem.add_rule("IC -> If BP Then AL", lambda i, bp, t, al: incompleteCommand("conditional", "thats it", ifCommand(bp, al + ["?"])))
sem.add_rule("IC -> IfCommand Else", lambda i, e: incompleteCommand("conditional", "thats it", ifElseCommand(i[0], i[1], "?")))
sem.add_rule("IC -> IfCommand Else AL", lambda i, e, al: incompleteCommand("conditional", "thats it", ifElseCommand(i[0], i[1], al + ["?"])))
# sem.add_rule("ConditionalCommand -> If I Say WP Then AL Thats It", lambda i, me, s, wp, then, al, thats, it: ifCommand(bp,al)) # todo

# Control Command

sem.add_rule("ControlCommand -> Wait NP Seconds", lambda waitt, unk, seconds: wait(unk))
sem.add_rule("ControlCommand -> Wait Until BP", lambda wait, until, bp: waitUntil(bp))
sem.add_rule("ControlCommand -> Repeat AL Until BP", lambda repeat, al, untill, bp: until(bp, al))
sem.add_rule("ControlCommand -> Repeat AL Forever", lambda repeat, al, forever: doForever(al))
sem.add_rule("ControlCommand -> Repeat AL Unk Times", lambda repeatt, al, unk, times: repeat(unk, al))
sem.add_rule("ControlCommand -> Delete Det Clone", lambda delete, this, clone: deleteClone())

#LoopCommand
sem.add_rule("Repeat -> Repeat The Steps", lambda r, t, s: r)
sem.add_rule("Repeat -> Repeat The Following Steps", lambda r, t, f, s: r)
sem.add_rule("Repeat -> Repeat The Following", lambda r, t, f: r)

sem.add_rule("LoopCommand -> Repeat AL Duration Thats It", lambda r, lcp, d, t, i: repeat_action_list(lcp, d))
sem.add_rule("LoopCommand -> Repeat Duration AL Thats It", lambda r, d, lcp, t, i: repeat_action_list(lcp, d))
sem.add_rule("LoopCommand -> AL Should Be Repeated Duration", lambda action_list,s,b,r, duration: repeat_action_list(action_list, duration))

# sem.add_rule("LoopCommand -> Repeat LoopCommandP", lambda r, lcp: lcp)
# sem.add_rule("LoopCommand -> LoopCommandP", identity)
# sem.add_rule("LoopCommand -> AL Should Be Repeated Duration", lambda action_list, t,s,b,r, duration: repeat_action_list(action_list, duration))
# sem.add_rule("LoopCommandP -> AP Duration", lambda ap, duration: repeat_action_list([ap], duration))
# sem.add_rule("LoopCommandP -> The Following Duration AL Thats It", lambda t, f, duration, action_list, tt, i: repeat_action_list(action_list, duration))
# sem.add_rule("LoopCommandP -> The Following Steps Duration AL Thats It", lambda t, f, s, duration, action_list, tt, i: repeat_action_list(action_list, duration))

sem.add_rule("IC -> Repeat", lambda r: incompleteCommand("loop", "thats it", repeat_action_list("?", "?")))
sem.add_rule("IC -> Repeat AL", lambda r, a: incompleteCommand("loop", "thats it", repeat_action_list(a, "?")))
sem.add_rule("IC -> Repeat Duration", lambda r, d: incompleteCommand("loop", "thats it", repeat_action_list("?", d)))
# sem.add_rule("IC -> The Following", lambda t, f: incompleteCommand("loop", "thats it", repeat_action_list("?", "?")))
# sem.add_rule("IC -> The Following Steps", lambda t, f, s: incompleteCommand("loop", "thats it", repeat_action_list("?", "?")))
# sem.add_rule("IC -> The Following Duration", lambda t, f, d: incompleteCommand("loop", "thats it", repeat_action_list("?", d)))
# sem.add_rule("IC -> The Following Steps Duration", lambda t, f, s, d: incompleteCommand("loop", "thats it", repeat_action_list("?", d)))
sem.add_rule("IC -> Repeat AL Duration", lambda r, a, d: incompleteCommand("loop", "thats it", repeat_action_list(a, d)))
sem.add_rule("IC -> Repeat Duration AL", lambda r, d, a: incompleteCommand("loop", "thats it", repeat_action_list(a, d)))
# sem.add_rule("IC -> The Following Duration AL", lambda t, f, d, a: incompleteCommand("loop", "thats it", repeat_action_list(a, d)))
# sem.add_rule("IC -> The Following Steps Duration AL", lambda t, f, s, d, a: incompleteCommand("loop", "thats it", repeat_action_list(a, d)))
sem.add_rule("IC -> AL Should Be Repeated", lambda a,s,b,r: incompleteCommand("loop", "times", repeat_action_list(a, "?")))

#General switches
sem.add_rule("To -> To Be", lambda t, b: t)



#####################################################################
## Lexicon

## Determiners
sem.add_lexicon_rule("Det", ['the', 'this', 'a', 'an'], lambda word: lambda: None)

## Noun - pronouns
sem.add_lexicon_rule("I", ["i"], identity)
sem.add_lexicon_rule("You",['you'],identity)
sem.add_lexicon_rule("Your",['your'],identity)
sem.add_lexicon_rule("My",['my'],identity)
sem.add_lexicon_rule("Myself",['myself'],identity)
sem.add_lexicon_rule("It", ["it"], identity)

## Noun - names
sem.add_lexicon_rule('NAME_OF_SOUND',
					 ['meow','cave','boing','chomp','drum','jungle','hey'],
					 # TODO: the semantic rule for NAME_OF_SOUND could involve
					 # searching
					 lambda name: name)
sem.add_lexicon_rule('LANGUAGE_NAME',
	['english', 'danish', 'dutch', 'french', 'german', 'italian', 'japanese', 'russian'], lambda language: language.capitalize())
sem.add_lexicon_rule('VOICE_NAME', ['quinn', 'max', 'squeak', 'giant', 'kitten'], identity)
sem.add_lexicon_rule("Direction",['up', 'left', 'right', 'down'],identity)
sem.add_rule("KEY_NAME -> Direction Arrow", lambda d, a: d+" "+a)

sem.add_lexicon_rule("Unk", ['0','1','2','3','4','5','6','7','8','9'], identity)
sem.add_lexicon_rule("SequenceAdverb", ['then', 'after', 'finally'], identity)

sem.add_lexicon_rule("DRUM", ['tambourine', 'claves', 'cowbell', 'triangle', 'bongo', 'conga', 'cabasa', 'guiro', 'vibraslap', 'cuica'], identity)
sem.add_lexicon_rule("Drum1", ['snare', 'bass', 'side', 'crash', 'open', 'closed', 'hand', 'wood'], identity)
sem.add_lexicon_rule("Drum2", ['drum', 'stick', 'cymbal', 'highhat', 'hi', 'clap', 'block'], identity)
sem.add_lexicon_rule("Drum3", ['hat'], identity)

sem.add_lexicon_rule("INSTRUMENT", ['piano', 'organ', 'guitar', 'bass', 'pizzicato', 'cello', 'trombone', 'clarinet', 'saxophone', 'flute', 'bassoon', 'choir', 'vibraphone', 'marimba'], identity)
sem.add_lexicon_rule("Instrument1", ['electric', 'wooden', 'music', 'steel', 'synth'], identity)
sem.add_lexicon_rule("Instrument2", ['piano', 'guitar', 'flute', 'box', 'drum', 'lead', 'pad'], identity)


sem.add_lexicon_rule("OrderAdverb",
					   ['secondly', 'fourthly', 'fifthly', 'seventh', 'second', 'fifth', 'sixthly', 'third', 'thirdly', 'fourth', 'sixth', 'firstly', 'first'],
					   lambda word: wordMap(word))

## Noun - keywords

# Sounds
sem.add_lexicon_rule("Sounds", ['sounds'], identity)
sem.add_lexicon_rule("Sound", ['sound'], identity)
sem.add_lexicon_rule("Volume", ['volume'], identity)
sem.add_lexicon_rule("Pitch", ['pitch'], identity)
sem.add_lexicon_rule("Effect", ['effect'], identity)
sem.add_lexicon_rule("Percent", ['percent'], identity)
sem.add_lexicon_rule("Seconds", ['seconds'], identity)

# Events
sem.add_lexicon_rule("Arrow",['arrow'],identity)
sem.add_lexicon_rule("Green", ["green"], identity)
sem.add_lexicon_rule("Flag", ["flag"], identity)
sem.add_lexicon_rule("Message",['message'],identity)
sem.add_lexicon_rule("Key",['key', 'button'],identity)
sem.add_lexicon_rule("Program", ["program"], identity)

# Voice
sem.add_lexicon_rule("Response",['response', 'reply'],identity)
sem.add_lexicon_rule("Speech",['speech'],identity)

sem.add_lexicon_rule("Voice",['voice'],identity)
sem.add_lexicon_rule("Language",['language'],identity)
sem.add_lexicon_rule("Accent",['accent'],identity)

# Music
sem.add_lexicon_rule("Drum", ['drum', 'instrument'], identity)
sem.add_lexicon_rule("Beats", ['beats', 'beat'], identity)
sem.add_lexicon_rule("Note", ['note'], identity)
sem.add_lexicon_rule("Instrument", ['instrument'], identity)
sem.add_lexicon_rule("Tempo", ['tempo'], identity)

# Scratch specific
sem.add_lexicon_rule("Sprite", ["sprite"], identity)
sem.add_lexicon_rule("Sprites",['sprites'],identity)
sem.add_lexicon_rule("Backdrop", ["backdrop"], identity)
sem.add_lexicon_rule("Clone", ['clone'], identity)

# data & variables
sem.add_lexicon_rule("List", ["list"], identity)
sem.add_lexicon_rule("Variable",['variable'],identity)

## Verbs - Speech
sem.add_lexicon_rule("Listen",['listen'],identity)
sem.add_lexicon_rule("Hear",['hear'],identity)
sem.add_lexicon_rule("Say",['say', 'voice', 'speak'],identity) # TODO: is it safe to do map 'Say' To 'tell me', which has two words in it?
sem.add_lexicon_rule("Talk",['talk'],identity)


## Keywords
# Conditional Command Keywords
sem.add_lexicon_rule("If", ['if'], identity)
sem.add_lexicon_rule("Then", ['then'], identity)
sem.add_lexicon_rule("Else", ['else', 'otherwise'], identity)
sem.add_lexicon_rule("Thats", ["thats"], identity)
sem.add_lexicon_rule("Until", ['until', 'till'], identity)

## Algebra Command Keywords
sem.add_lexicon_rule("Equals", ["equals", "is"], identity)
sem.add_lexicon_rule("Equal", ["equal"], identity)
sem.add_lexicon_rule("Greater", ["greater"], identity)
sem.add_lexicon_rule("Less", ["less"], identity)

sem.add_lexicon_rule("Divided",['divided'],identity)
sem.add_lexicon_rule("Divide",['divide'],identity)
sem.add_lexicon_rule("Multiply",['multiply'],identity)
sem.add_lexicon_rule("Multiplied",['multiplied'],identity)
sem.add_lexicon_rule("Times",['times'],identity)
sem.add_lexicon_rule("Product",['product'],identity)
sem.add_lexicon_rule("Minus",['minus'],identity)
sem.add_lexicon_rule("Subtracted",['subtracted'],identity)
sem.add_lexicon_rule("Difference",['difference'],identity)
sem.add_lexicon_rule("Sum",['sum'],identity)
sem.add_lexicon_rule("Added",['added'],identity)
sem.add_lexicon_rule("Plus",['plus'],identity)
sem.add_lexicon_rule("Negative",['negative'],identity)

sem.add_lexicon_rule("Random",['random'],identity)
sem.add_lexicon_rule("Number",['number'],identity)

# Data Command Keywords
sem.add_lexicon_rule("Add", ["add", "append"], identity)
sem.add_lexicon_rule("Increment", ["increment", "increase"], identity)
sem.add_lexicon_rule("Decrement", ["decrement", "decrease"], identity)
sem.add_lexicon_rule("Subtract", ["subtract"], identity)
sem.add_lexicon_rule("Contains",['contains', 'has'],identity)
sem.add_lexicon_rule("Called",['called', 'named'],identity)
sem.add_lexicon_rule("Use", ['use'], identity)
sem.add_lexicon_rule("Set", ['set'], identity)
sem.add_lexicon_rule("Replace", ['replace'], identity)
sem.add_lexicon_rule("Change", ['change'], identity)
sem.add_lexicon_rule("Delete", ['delete'], identity)
sem.add_lexicon_rule("Ele",['element', 'item'],identity)
sem.add_lexicon_rule("Make",['make', 'create'],identity)

# Loop Command Keywords
sem.add_lexicon_rule("Repeat", ['repeat', 'do'], identity)
sem.add_lexicon_rule("Repeated", ['repeated', 'done'], identity)
sem.add_lexicon_rule("Forever",['forever'],identity)
sem.add_lexicon_rule("Duration", ['forever'],identity)
sem.add_lexicon_rule("Steps", ['steps'], identity)
sem.add_lexicon_rule("Times", ['times'], identity)

# Sound Command Keywords
sem.add_lexicon_rule("Softer",['softer', 'quieter'],identity)
sem.add_lexicon_rule("Louder",['louder'],identity)
sem.add_lexicon_rule("Slower",['slower'],identity)
sem.add_lexicon_rule("Faster",['faster'],identity)
sem.add_lexicon_rule("Play", ['play'], identity)
sem.add_lexicon_rule("Stop", ['stop', 'terminate'], identity)
sem.add_lexicon_rule("Wait", ['wait'], identity)

# Logic Keywords
sem.add_lexicon_rule("Or", ["or"], identity)
sem.add_lexicon_rule("And", ["and"], identity)
sem.add_lexicon_rule("NEG", ["not"], identity)
sem.add_lexicon_rule("NEG", ["isnt"], identity)# not working
sem.add_lexicon_rule("POS", ["is"], identity)
sem.add_lexicon_rule("TRUE", ["true"], identity)
sem.add_lexicon_rule("FALSE", ["false"], identity)
sem.add_rule("NEG -> Is NEG", lambda x, y: y)

# Event Keywords
sem.add_lexicon_rule("When", ["when"], identity)
sem.add_lexicon_rule("Whenever",['whenever'],identity)
sem.add_lexicon_rule("Clicked", ["pressed", "clicked"], identity)
sem.add_lexicon_rule("Starts", ["starts"], identity)
sem.add_lexicon_rule("Switches", ["switches"], identity)
sem.add_lexicon_rule("Receive", ["receive"], identity)
sem.add_lexicon_rule("Broadcast",['broadcast'],identity)

# Timer Keywords
sem.add_lexicon_rule("Timer", ["timer"], identity)
sem.add_lexicon_rule("Reset", ["reset", "zero", "restart", "initialize"], identity)

## Adj
sem.add_lexicon_rule("All",['all'],identity)
sem.add_lexicon_rule("Following",['following'],identity)
sem.add_lexicon_rule("Same", ["same"], identity)
sem.add_lexicon_rule("New",['new'],identity)
sem.add_lexicon_rule("Every",['every', 'each'],identity)
sem.add_lexicon_rule("Single",['single'],identity)
sem.add_lexicon_rule("Time", ["time"], identity)

## Other random words
sem.add_lexicon_rule("Should", ['should'], identity)
sem.add_lexicon_rule("Too", ["too", "simultaneously"], identity)
sem.add_lexicon_rule("Between",['between'],identity)
sem.add_lexicon_rule("From",['from'],identity)
sem.add_lexicon_rule("With",['with'],identity)
sem.add_lexicon_rule("Than", ["than"], identity)
sem.add_lexicon_rule("Is", ["is"], identity)
sem.add_lexicon_rule("At", ["at"], identity)
sem.add_lexicon_rule("In", ["in"], identity)
sem.add_lexicon_rule("For", ['for'],identity)
sem.add_lexicon_rule("Of", ['of', 'from'],identity)
sem.add_lexicon_rule("That", ["that"], identity)
sem.add_lexicon_rule("Be", ["be"], identity)
sem.add_lexicon_rule("The", ["the"], identity)
sem.add_lexicon_rule("This", ["this"], identity)
sem.add_lexicon_rule("To",['to'],identity)
sem.add_lexicon_rule("By",['by'],identity)
sem.add_lexicon_rule("As",['as'],identity)
sem.add_lexicon_rule("Can",['can', 'could', 'may'],identity)
sem.add_lexicon_rule ("Please",['please'],identity)

sem.add_lexicon_rule("BACKDROP_NAME",['Space'],identity)



## Synonyms
def processSynonyms(synonyms):
	single_word_synonyms = []
	multi_word_synonyms = []
	for syn in synonyms:
		if '_' in syn:
			#multi-word synonym
			this_synonym =  syn.split('_')
			if len(this_synonym) == 2:
				#each multi word synonym is an array where each element is each word
				multi_word_synonyms.append(this_synonym)
		else:
			single_word_synonyms.append(syn)
	return single_word_synonyms, multi_word_synonyms
def findAndAddSynonymToGrammar(nonterminal, terminal, terminalType):
	synonyms = findSynonyms(terminal, terminalType)
	singleWordList, multiWordList = processSynonyms(synonyms)
	# add singleword synonym list
	addSynToLexiconRule(nonterminal, terminal, terminalType, singleWordList)
	# add multi word synonym list
	# if list is non empty
	if multiWordList:
		for multiWordSyn in multiWordList:
			#currently only handle multiWordSyn that are 2 words(which should be 99% of the case)
			parents = [word.upper() for word in multiWordSyn]
			#create non terminal nodes representing each word in multiword synonym
			syntacticRule = nonterminal+" -> " + parents[0] + " " + parents[1]
		#print("syntacticRule",syntacticRule,multiWordSyn[0],multiWordSyn[1])
			#returning none since these words aren't important in the script generation
			sem.add_rule(syntacticRule, lambda f, s: "none")
			sem.add_lexicon_rule(parents[0], [multiWordSyn[0]], identity)
			sem.add_lexicon_rule(parents[1], [multiWordSyn[1]], identity)

def addSynToLexiconRule(nonterminal, terminal, terminalType, synonyms):
	# add to lexicon iff length of synonym>=1 and synonyms don't only contain
	# the word itself
	if len(synonyms) > 0:
		if len(synonyms) != 1:
			sem.add_lexicon_rule(nonterminal, synonyms, identity)
		else:
			if (synonyms[0] != terminal):
				sem.add_lexicon_rule(nonterminal, synonyms, identity)

eligibleWords = [
	["Increment", "increment", wn.VERB],
	["Decrement", "decrement", wn.VERB],
	["Subtract", "subtract", wn.VERB],
	["Sprite", "sprite", wn.NOUN],
	["Play", "play", wn.VERB],
	["Replace", "replace", wn.VERB],
	["Change", "change", wn.VERB],
	["Stop", "stop", wn.VERB],
	["Wait", "wait", wn.VERB],
	["Repeat", "repeat", wn.VERB],
	["Delete", "delete", wn.VERB],
	["Make", "create", wn.VERB],
	["Make", "generate", wn.VERB],
	["Reset", "reset", wn.VERB],
	["Timer", "timer", wn.NOUN],
	["Time", "time", wn.NOUN],
	["Sound", "sound", wn.NOUN],
	["Message", "message", wn.NOUN],
	["Forever", "forever", wn.ADV],
	["Flag", "flag", wn.NOUN],
	["Receive", "receive", wn.VERB],
	["Equal", "equal", wn.ADJ],
	["Greater", "greater", wn.ADJ],
	["Less", "less", wn.ADJ],
	["Broadcast", "broadcast", wn.VERB]
]
for e_word in eligibleWords:
	findAndAddSynonymToGrammar(e_word[0], e_word[1], e_word[2])
