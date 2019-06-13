# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'../software/')
sys.path.insert(0,'../../software/')
import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry

from nltk.corpus import wordnet as wn
from text2num import text2int

sys.path.insert(0,'../server/flaskr')
import random
from sounds import get_sounds

############################synonym helpers #########################

class SynonymHelper():
	def __init__(self):
		self.eligible_words = [
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

	# Given a SemanticRuleSet object, update the grammar to include synonyms for
	# the eligible words.
	def update_grammar(self, sem):
		for e_word in self.eligible_words:
			self._find_and_add_synonym_to_grammar(sem, e_word[0], e_word[1], e_word[2])

	def _process_synonyms(self, synonyms):
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

	def _find_and_add_synonym_to_grammar(self, sem, nonterminal, terminal, terminalType):
		synonyms = self._find_synonyms(terminal, terminalType)
		singleWordList, multiWordList = self._process_synonyms(synonyms)
		# add singleword synonym list
		self._add_syn_to_lexicon_rule(sem, nonterminal, terminal, terminalType, singleWordList)
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
				sem.add_lexicon_rule(parents[0], [multiWordSyn[0]], lambda x:x)
				sem.add_lexicon_rule(parents[1], [multiWordSyn[1]], lambda x:x)

	def _add_syn_to_lexicon_rule(self, sem, nonterminal, terminal, terminalType, synonyms):
		# add to lexicon iff length of synonym>=1 and synonyms don't only contain
		# the word itself
		if len(synonyms) > 0:
			if len(synonyms) != 1:
				sem.add_lexicon_rule(nonterminal, synonyms, lambda x:x)
			else:
				if (synonyms[0] != terminal):
					sem.add_lexicon_rule(nonterminal, synonyms, lambda x:x)

	def _get_words_in_synset(self, synset):
		words = set()
		lemmas = synset.lemmas()
		for lemma in lemmas:
			this_synonym = str(lemma.name())
			words.add(this_synonym)
		return words

	def _find_synonyms(self, word, part_of_speech):
		synonyms = set()
		synsets_found = wn.synsets(word, part_of_speech)
		for synset in synsets_found:
			current_synset_synonyms = self._get_words_in_synset(synset)
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

class CodiSemanticRuleSet(SemanticRuleSet):
	def __init__(self):
		SemanticRuleSet.__init__(self);
		self.variables = {}
		self.lists = {}
		self.sounds = set()
		self.setup()

	def identity(self, x):
		return x

	####################################################################
	# Music Actions
	def soundToNumber(self, string):
		sounds = {"snare drum": 1, "bass drum": 2, "side stick": 3, "crash cymbal": 4, "open hi hat": 5, "open highhat": 5, "closed hi hat": 6, "closed highhat": 6, "tambourine": 7, "hand clap": 8, "claves": 9, "wood block": 10, "cowbell": 11, "triangle": 12, "bongo": 13, "conga": 14, "cabasa": 15, "guiro": 16, "vibraslap": 17, "cuica": 18}
		if string in sounds:
			# Add the sound to the project.
			self.sounds.add(string)
			# Return the number corresponding to desired sound.
			return sounds[string]
		else:
			## TODO RAISE ERROR
			return 1

	def playInstrumentBeats(self, sound, beats):
		# Add the sound to the project.
		self.sounds.add(sound)
		return ["playDrum", sound, beats]

	def rest(self, numberOfBeats):
		return ['rest:elapsed:from:', numberOfBeats]

	def InstrumentToNumber(self, string):
		sounds = {"piano": 1, "electric piano": 2, "organ": 3, "guitar": 4, "electric guitar": 5, "bass": 6, "pizzicato": 7, "cello": 8, "trombone": 9, "clarinet": 10, "saxophone": 11, "flute": 12, "wooden flute": 13, "bassoon": 14, "choir": 15, "vibraphone": 16, "music box": 17, "steel drum": 18, "marimba": 18, "synth lead": 20, "synth pad": 21}
		if string in sounds:
			# Add the sound to the project.
			self.sounds.add(string.title())
			return sounds[string]
		else:
			## TODO RAISE ERROR
			return 0

	def setInstrument(self, num):
		return ["instrument:", num]

	def playNoteDuration(self, note, duration):
		return ["noteOn:duration:elapsed:from:", note, duration]

	def setTempo(self, num):
		return ["setTempoTo:", num]

	def changeTempo(self, num):
		return ["changeTempoBy:", num]

	# Speech Actions
	def processSentence(self, data):
		if len(data) > 0:
			data = [thing for thing in data if thing != None]
			return {'scripts': data, 'variables': self.variables, 'lists': self.lists, 'sounds': self.sounds}

	def singleCommand(self, commandName, value):
		return [commandName, value]

	def singleCommandNoValue(self, commandName):
		return [commandName]

	def playSound(self, name):
		# Add the sound to the project.
		self.sounds.add(name.title())
		return ["doPlaySoundAndWait", name.title()]

	def startSound(self, name):
		# Add the sound to the project.
		self.sounds.add(name.title())
		return ["playSound:", name.title()]

	def ifCommand(self, if_cond, if_body):
		return ["doIf", if_cond, if_body]

	def ifElseCommand(self, if_cond, if_body, else_body):
		return ["doIfElse", if_cond, if_body, else_body]


	def repeat(self, num_times, repeat_body):
		return ["doRepeat", int(num_times), [repeat_body]]

	def until(self, until_condition, repeat_body):
		return ["doUntil", until_condition, [repeat_body]]

	def doForever(self, forever_body):
		return ["doForever", [forever_body]]

	def deleteClone(self):
		return ["deleteClone"]


	def wait(self, wait_time):
		return ["wait:elapsed:from:", wait_time]

	def waitUntil(self, until_condition):
		return ["doWaitUntil", until_condition]

	def getNumber(self, unk):
			try:
				num = int(unk)
			except:
				try:
					num = float(unk)
				except:
					num = text2int(unk)
			return num

	def setVariable(self, var_name, value):
		#self.variables[var_name] = value
		return ["setVar:to:",var_name, value]

	def logVariable(self, var_name):
		if (var_name in self.variables):
			whatToSay = var_name + " is " + str(getValue(var_name))
		else:
			whatToSay = "You don't have a variable called " + var_name
		return ["speakAndWait:", whatToSay]

	def deleteVariable(self, variable_name):
		del self.variables[variable_name]
		return wait(0.1)

	def createVariable(self, variable_list):
		for var in variable_list:
			self.variables[var] = 0
		return wait(0.1)
			# TODO: somehow prevent returning the variable name in response of processSentence.
		#return None

	def createSingleList(self, name):
		self.lists[name] = []
		return wait(0.1)


	def createClone(self):
		return ["createCloneOf:", "myself"]

	def itemInList(self, unk, name):
		return ["list:contains:", name, unk]

	def resetTimer(self):
		return ["timerReset"]

	# OPERATORS
	def add(self, n1, n2):
		return ['+', n1, n2]

	def subtract(self, n1, n2):
		return ['-', n1, n2]

	def getProduct(self, num, num2):
		return ["*", num, num2]

	def getQuotient(self, num, num2):
		return ["/", num, num2]

	def getValue(self, var):
		return ["readVariable", var]

	def getRandomNumberBetween(self, unk1, unk2):
		return ['randomFrom:to:', unk1, unk2]

	def getRandomSound(self):
		sound = random.choice(get_sounds())
		return sound["soundName"]

	def lessThan(self, a,b):
		return ["<", a, b]

	def greaterThan(self, a,b):
		return [">", a, b]

	def equalTo(self, a,b):
		return ["=", a, b]

	def GEQ(self, a,b):
		return ["|", [">", a, b], ["=", a, b]]

	def LEQ(self, a,b):
		return ["|", ["<", a, b], ["=", a, b]]

	def logicOr(self, b1, b2):
		return ["|", b1, b2]

	def logicAnd(self, b1, b2):
		return ["&", b1, b2]

	def waitTillTimer(self, x):
		return ["doWaitUntil", x]

	def negate(self, unk):
		return ["*", unk, -1]

	def changeVarBy(self, var_name, unk, opt_negate=False):
		if opt_negate:
			return ["changeVar:by:", var_name, ["*", unk, -1]]
		return ["changeVar:by:",var_name, unk]

	def changeVarbyVar(self, var1, var2,opt_negate=False):
		if opt_negate:
			return ["setVar:to:", var1, ["*", getValue(var2), -1]]
		return ["changeVar:by:", var1, getValue(var2)]

	def ynQuestion(self, data):
		if self.learned.yesno_query(data):
			return "Yes."
		else:
			return "No."

	def whenYouHear(self, word_phrase):
		return ["whenIHear", word_phrase]

	def whenGreenFlag(self):
		return ["whenGreenFlag"]

	def whenKeyClicked(self, name):
		return ["whenKeyPressed", name]

	def whenClicked(self):
		return ["whenClicked"]

	def whenBackSwitch(self, name):
		return ["whenSceneStarts", name]

	def whenReceive(self, message):
		return ["whenIReceive", message]

	def broadcastMessage(self, name):
		return ["broadcast:", name]

	def broadCastMessageWait(self, name):
		return ["doBroadcastAndWait:", name]

	def not_identity(self, x):
		return ["not", x]

	def SimpleEvent(self, e, a):
		# flatten the action list
		return [e] + a

	def whQuestion(self, data):
		results = self.learned.wh_query(data)
		if len(results) == 0:
			return "I don't know."
		else:
			return list(results)[0]

	def npOnlyHuhResponse(self, data):
		return "What about %s?"%(pretty_print_entry(data))

	# List commands
	def getItem(self, ind, list_name):
		return ['getLine:ofList:', ind, list_name]

	def wordMap(self, order_adverb):
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

	def addToList(self, list_name, item):
		return ['append:toList:', item, list_name]

	def deleteListItem(self, list_name, ind):
		return ['deleteLine:ofList:', ind, list_name]

	def setItemInList(self, ind, list_name, item):
		return ['setLine:ofList:to:', ind, list_name, item]

	# Loop commands
	def repeat_action_list(self, action_list, duration):
		if duration == 'forever':
			return ['doForever', action_list]
		else:
			return ['doRepeat', duration, action_list]

	def get_duration(self, duration):
			return duration

	# Sequential commands
	def appendToProgram(self, action_list):
		program.append(action_list)
		return action_list


	def getAP(self, phrase):
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

	def setup(self):
		self.add_rules()
		synonym_helper = SynonymHelper()
		synonym_helper.update_grammar(self)

	def add_rules(self):
		# Start rules
		self.add_rule("Start -> S", lambda s: self.processSentence(s))

		# All Command
		self.add_rule("S -> AL", self.identity)
		self.add_rule("AL -> AP", lambda p: self.getAP(p))
		self.add_rule("AL -> AP AL", lambda p, l: [p]+l)
		self.add_rule("AL -> AP And AL", lambda p,an, l: [p]+l)

		self.add_rule("AP -> Text2SpeechCommand", self.identity)
		self.add_rule("AP -> Speech2TextCommand", self.identity)
		self.add_rule("AP -> MusicCommand", self.identity)
		self.add_rule("AP -> SoundCommand", self.identity)
		self.add_rule("AP -> CreateCommand", self.identity)
		self.add_rule("AP -> DataCommand", self.identity)
		self.add_rule("AP -> EventHandler", self.identity)
		# self.add_rule("AP -> EventHandler", lambda eventHandler: [111,124, eventHandler])
		#self.add_rule("AP -> SequentialCommand", self.identity)
		self.add_rule("AP -> ConditionalCommand", self.identity)
		self.add_rule("AP -> LoopCommand", self.identity)
		self.add_rule("AP -> TimerCommand", self.identity)
		self.add_rule("AP -> BroadcastCommand", self.identity)
		self.add_rule("AP -> ControlCommand", self.identity)
		self.add_rule("AL -> SequentialCommand", self.identity)
		self.add_rule("AL -> OrderedCommand", self.identity)

		# Ordered Command
		self.add_rule("OrderedCommand -> OrderAdverb AL", lambda num, al: al)

		# SequentialCommand
		self.add_rule("SequentialCommand -> SequenceAdverb AL", lambda seq_adv, action_list: action_list)

		# Create Command
		self.add_rule("CreateCommand -> Make Det Clone Of Myself", lambda m, det, c,o, my: self.createClone())
		self.add_rule("CreateCommand -> Make VARIABLE_LIST", lambda make, vl: self.createVariable(vl))
		self.add_rule("CreateCommand -> Make LIST_NAME", lambda make, name: self.createSingleList(name))

		# Variable Handling
		self.add_rule("VARIABLE_LIST -> VARIABLE_NAME", lambda vl: [vl])
		self.add_rule("VARIABLE_LIST -> VARIABLE_NAME And VARIABLE_LIST", lambda vn, a, vl: [vn]+vl)
		self.add_rule("VARIABLE_NAME -> Variable VARIABLE_NAME", lambda l, name: name)
		self.add_rule("Variable -> Det Variable", lambda det, var: None)
		self.add_rule("Variable -> Your Variable", lambda det, var: None)
		self.add_rule("Variable -> My Variable", lambda det, var: None)
		self.add_rule("Variable -> Variable Called", lambda v, c: None)
		self.add_rule("Variable -> New Variable", lambda v, c: None)

		# List Handling
		self.add_rule("LIST_NAME -> List LIST_NAME", lambda l, name: name)
		self.add_rule("List -> Det List", lambda det, liss: None)
		self.add_rule("List -> Your List", lambda det, liss: None)
		self.add_rule("List -> My List", lambda det, liss: None)
		self.add_rule("List -> New List", lambda det, liss: None)
		self.add_rule("List -> List Called", lambda liss, c: None)

		self.add_rule("KEY_NAME -> KEY_NAME Key", lambda name, key: name)
		self.add_rule("KEY_NAME -> Det KEY_NAME", lambda det, name: name)
		self.add_rule("KEY_NAME -> Direction Key", lambda name, key: name+" arrow")

		self.add_rule("ITEM -> NP", lambda i:i)
		self.add_rule("ITEM -> MESSAGE_NAME", lambda name: name)
		self.add_rule("ITEM -> BP", lambda name: name)
		#self.add_rule("ITEM -> VARIABLE_NAME", lambda name: name)
		self.add_rule("ITEM -> DATA_REPORTER", self.identity)

		self.add_rule("ITEM -> WP", lambda i:i) # Word phrase

		self.add_rule("WP -> WP_1", lambda i:i) # Speech phrase
		self.add_rule("WP -> WP_2", lambda i:i) # Speech phrase
		self.add_rule("WP_1 -> SP", lambda i:i) # Speech phrase
		self.add_rule("WP_2 -> Word", lambda unk:unk) # Word phrase can map to what someone said.
		self.add_rule("WP_2 -> Word WP_2", lambda w1, wp : ' '.join([w1, wp])) # Word phrase can map to what someone said.

		# Duration
		self.add_rule("Duration -> NP Times", lambda np, times: self.get_duration(np))

		# Speech2Text Commands
		self.add_rule("Speech2TextCommand -> Listen And Wait", lambda l, a, w: self.singleCommandNoValue("listenAndWait"))
		self.add_rule("Speech2TextCommand -> Wait For Det Response", lambda w, f, d, r: self.singleCommandNoValue("listenAndWait"))
		self.add_rule("Speech2TextCommand -> Wait For Det Response", lambda w, f, d, r: self.singleCommandNoValue("listenAndWait"))
		self.add_rule("SP -> Det Speech", lambda t, speech: self.singleCommandNoValue("getSpeech"))
		# self.add_rule("EVENT -> When You Hear WP", lambda w, y, hear, wp: self.whenYouHear(wp))
		# self.add_rule("EVENT -> When I Say WP", lambda w, y, hear, wp: self.whenYouHear(wp))
		self.add_rule("EVENT -> Every Time You Hear WP", lambda e, t, y, hear, wp: self.whenYouHear(wp))
		self.add_rule("EVENT -> Every Time I Say WP", lambda e, t, i, say, wp: self.whenYouHear(wp))
		self.add_rule("EVENT -> Whenever You Hear WP", lambda we, y, hear, wp: self.whenYouHear(wp))
		self.add_rule("EVENT -> Whenever I Say WP", lambda we, i, say, wp: self.whenYouHear(wp))

		# Text2Speech Commands
		self.add_rule("Voice -> Det Voice", lambda d, v: v)
		self.add_rule("Voice -> Your Voice", lambda d, v: v)
		self.add_rule("Voice -> My Voice", lambda d, v: v)
		self.add_rule("VOICE_NAME -> Your VOICE_NAME Voice", lambda y, voice_name, v: voice_name)
		self.add_rule("VOICE_NAME -> Det VOICE_NAME Voice", lambda d, voice_name, v: voice_name)
		self.add_rule("VOICE_NAME -> VOICE_NAME Voice", lambda voice_name, v: voice_name)
		self.add_rule("VOICE_NAME -> Voice Called VOICE_NAME", lambda v, c, voice_name: voice_name)
		self.add_rule("VOICE_NAME -> Voice Of VOICE_NAME", lambda v, c, voice_name: voice_name)

		self.add_rule("Text2SpeechCommand -> Say The Speech", lambda s, t, speech: self.singleCommand("speakAndWait:", self.singleCommandNoValue("getSpeech")))
		self.add_rule("Text2SpeechCommand -> Say WP", lambda s, wp: self.singleCommand("speakAndWait:", wp))
		self.add_rule("Text2SpeechCommand -> Set Voice To VOICE_NAME", lambda s, v, t, voice_name: self.singleCommand("setVoice:", voice_name))
		self.add_rule("Text2SpeechCommand -> Change Voice To VOICE_NAME", lambda c, v, t, voice_name: self.singleCommand("setVoice:", voice_name))
		self.add_rule("Text2SpeechCommand -> Use VOICE_NAME", lambda u, voice_name: self.singleCommand("setVoice:", voice_name))
		self.add_rule("Text2SpeechCommand -> Switch Voice To VOICE_NAME", lambda s, v, t, voice_name: self.singleCommand("setVoice:", voice_name))

		self.add_rule("AccentP -> Det Accent", lambda d, acc: acc)
		self.add_rule("AccentP -> Accent", lambda acc: acc)
		self.add_rule("AccentP -> Your Accent", lambda y, acc: acc)
		self.add_rule("AccentP -> My Accent", lambda y, acc: acc)
		self.add_rule("LANGUAGE_NAMEP -> Accent Called LANGUAGE_NAME", lambda a, c, acc: acc)
		self.add_rule("LANGUAGE_NAMEP -> Accent For LANGUAGE_NAME", lambda a, f, acc: acc)
		self.add_rule("LANGUAGE_NAMEP -> Accent Of LANGUAGE_NAME", lambda a, f, acc: acc)
		self.add_rule("LANGUAGE_NAMEP -> LANGUAGE_NAME", lambda acc: acc)

		self.add_rule("Text2SpeechCommand -> Set AccentP To LANGUAGE_NAMEP", lambda s, l, t, language: self.singleCommand("setLanguage:", language))
		self.add_rule("Text2SpeechCommand -> Talk With Det LANGUAGE_NAME Accent", lambda t, w, d, language, ac: self.singleCommand("setLanguage:", language))
		self.add_rule("Text2SpeechCommand -> Change AccentP To LANGUAGE_NAMEP", lambda c, acc, t, language: self.singleCommand("setLanguage:", language))
		self.add_rule("Text2SpeechCommand -> Use Det LANGUAGE_NAME Accent", lambda u, d, language, a: self.singleCommand("setLanguage:", language))
		self.add_rule("Text2SpeechCommand -> Switch AccentP To LANGUAGE_NAMEP", lambda s, a, t, language: self.singleCommand("setLanguage:", language))

		# Music Command
		self.add_rule('DRUM -> Drum1 Drum2', lambda i, i2: i + ' ' + i2)
		self.add_rule('DRUM -> Drum1 Drum2 Drum3', lambda i, i2, i3: i + ' ' + i2 + ' ' + i3)
		self.add_rule('DRUM -> DRUM Drum', lambda i, d: i)
		self.add_rule('DRUM -> Drum DRUM', lambda d, i: i)
		self.add_rule('DRUM -> Det DRUM', lambda d, i: i)

		self.add_rule('INSTRUMENT -> Instrument1 Instrument2', lambda i, i2: i + ' ' + i2)
		self.add_rule('INSTRUMENT -> Det INSTRUMENT', lambda d, i: i)
		self.add_rule('INSTRUMENT -> Instrument INSTRUMENT', lambda i, instrument: instrument)
		self.add_rule('Note -> Det Note', lambda d, i: i)

		self.add_rule('MusicCommand -> Use INSTRUMENT', lambda u, i: self.setInstrument(self.InstrumentToNumber(i)))
		self.add_rule('MusicCommand -> Set Instrument To INSTRUMENT', lambda s, i, t, ii: self.setInstrument(self.InstrumentToNumber(ii)))
		self.add_rule('MusicCommand -> Set Det Instrument To INSTRUMENT', lambda s, d, i, t, ii: self.setInstrument(self.InstrumentToNumber(ii)))
		self.add_rule('MusicCommand -> Use INSTRUMENT As Det Instrument', lambda u, ii, a, d, i: self.setInstrument(self.InstrumentToNumber(ii)))
		self.add_rule('MusicCommand -> Play INSTRUMENT', lambda p, i: self.setInstrument(self.InstrumentToNumber(i)))
		self.add_rule('MusicCommand -> Play Note NP For NP Beats ', lambda p, n, note, f, beats, b: self.playNoteDuration(note, beats))

		self.add_rule('Tempo -> Det Tempo', lambda d, t: t)
		# It doesn't actually matter what BPM returns.
		self.add_rule('BPM -> Beats Per Minute', lambda b, p, m: b)
		self.add_rule('MusicCommand -> TempoCommand BPM', lambda tc, bpm: tc)
		self.add_rule('MusicCommand -> TempoCommand', lambda tc: tc)
		self.add_rule('TempoCommand -> Set Tempo To NP ', lambda s, tempo, t, n: self.setTempo(n))
		self.add_rule('TempoCommand -> Change Tempo By NP ', lambda s, tempo, t, n: self.changeTempo(n))
		self.add_rule('TempoCommand -> Increment Tempo By NP ', lambda i, tempo, t, n: self.changeTempo(n))
		self.add_rule('TempoCommand -> Decrement Tempo By NP ', lambda d, tempo, t, n: self.changeTempo(negate(n)))

		self.add_rule('MusicCommand -> Play DRUM For NP Beats' , lambda p, i, f, n, b: self.playInstrumentBeats(self.soundToNumber(i), n))
		self.add_rule('MusicCommand -> Play DRUM NP Beats' , lambda p, i, n, b: self.playInstrumentBeats(self.soundToNumber(i), n))
		self.add_rule('MusicCommand -> Rest For NP Beats' , lambda r, f, numberOfBeats, b: self.rest(numberOfBeats))


		# Sound Command
		# Use the halting version of the play sound block
		self.add_rule("SoundCommand -> SStart NAME_OF_SOUND", lambda start, name: self.startSound(name))
		self.add_rule("SoundCommand -> Play NAME_OF_SOUND", lambda play, name: self.playSound(name))

		# TODO(quacht): instead of just using name.title(), use a helper method to select the sound that might match best?
		# TODO(quacht): at the same time, verify that the sound actually belongs to the sound library.
		self.add_rule("NAME_OF_SOUND -> Det NAME_OF_SOUND", lambda d, name: name.title())
		self.add_rule("NAME_OF_SOUND -> Your NAME_OF_SOUND", lambda d, name: name.title())
		self.add_rule("NAME_OF_SOUND -> NAME_OF_SOUND Sound", lambda name, sound: name.title())
		self.add_rule("NAME_OF_SOUND -> Sound Called NAME_OF_SOUND", lambda s, c, name: name.title())
		self.add_rule("NAME_OF_SOUND -> Random Sound", lambda r, s: self.getRandomSound())
		# Some sounds may consist of names that have 2 or 3 words in them.
		self.add_rule("NAME_OF_SOUND -> Unk Unk", lambda unk1, unk2: unk1 + ' ' + unk2)
		self.add_rule("NAME_OF_SOUND -> Unk Unk Unk", lambda unk1, unk2, unk3: unk1 + ' ' + unk2 + ' ' + unk3)

		self.add_rule("SoundCommand -> Set TheVolume To NP", lambda sett, volume, too, unk: self.singleCommand("setVolumeTo:", unk))
		self.add_rule("SoundCommand -> Set TheVolume To NP Percent", lambda sett, volume, too, unk, percent: self.singleCommand("setVolumeTo:", unk))

		self.add_rule("SoundCommand -> Change TheVolume By NP", lambda change, volume, by, Unk: self.singleCommand("changeVolumeBy:", Unk))
		self.add_rule("SoundCommand -> Change TheVolume By NP Percent", lambda change, volume, by, Unk, p: self.singleCommand("changeVolumeBy:", Unk))
		self.add_rule("SoundCommand -> Increment TheVolume By NP", lambda change, volume, by, Unk: self.singleCommand("changeVolumeBy:", Unk))

		self.add_rule("SoundCommand -> Decrement TheVolume By NP", lambda change, volume, by, Unk: self.singleCommand("changeVolumeBy:", self.negate(Unk)))
		self.add_rule("SoundCommand -> Decrement TheVolume By NP Percent", lambda change, volume, by, Unk, p: self.singleCommand("changeVolumeBy:", self.negate(Unk)))

		self.add_rule("SoundCommand -> Change ThePitch Effect By NP", lambda change, pitch, effect, by, Unk: self.singleCommand("changeTempoBy:", Unk))

		self.add_rule("TheVolume -> The Volume", lambda d, v: v)
		self.add_rule("TheVolume -> Volume", self.identity)
		self.add_rule("ThePitch -> The Pitch", lambda d, v: v)
		self.add_rule("ThePitch -> Pitch", self.identity)

		self.add_rule("SoundCommand -> Stop All Sounds", lambda stop, all, sounds: self.singleCommandNoValue("stopAllSounds"))
		self.add_rule("SoundCommand -> Stop", lambda stop: self.singleCommandNoValue("stopAllSounds"))
		self.add_rule("SoundCommand -> Softer", lambda softer: self.singleCommand("changeVolumeBy:", -10))
		self.add_rule("SoundCommand -> Louder", lambda louder: self.singleCommand("changeVolumeBy:", 10))
		self.add_rule("SoundCommand -> Slower", lambda slower: self.singleCommand("changeTempoBy:", -10))
		self.add_rule("SoundCommand -> Faster", lambda faster: self.singleCommand("changeTempoBy:", 10))


		## Data Command

		# todo: fix
		self.add_rule("DataCommand -> Log VARIABLE_NAME", lambda log, var_name: logVariable(var_name))
		self.add_rule("DataCommand -> Delete VARIABLE_NAME", lambda delete, var_name: deleteVariable(var_name))
		self.add_rule("DataCommand -> Set VARIABLE_NAME To BP", lambda s, var_name, to, bp: setVariable(var_name, bp))
		self.add_rule("DataCommand -> Set VARIABLE_NAME To NP", lambda s, var_name, to, np: setVariable(var_name, np))
		self.add_rule("DataCommand -> Set VARIABLE_NAME To ITEM", lambda s, var_name, to, item: setVariable(var_name, item))

		self.add_rule("DataCommand -> Add NP To VARIABLE_NAME", lambda a, num, t, var_name:
		changeVarBy(var_name, num))
		self.add_rule("DataCommand -> Increment VARIABLE_NAME By NP", lambda i, var_name, b, num: changeVarBy(var_name, num))
		self.add_rule("DataCommand -> Add VARIABLE_NAME To VARIABLE_NAME", lambda i, var1, b, var2: changeVarByVar(var2, getValue(var1)))

		self.add_rule("DataCommand -> Subtract NP From VARIABLE_NAME", lambda a, np, t, var_name: changeVarBy(var_name, np, 'negate'))
		self.add_rule("DataCommand -> Decrement VARIABLE_NAME By NP", lambda a, var_name, t, np: changeVarBy(var_name, np, 'negate'))
		self.add_rule("DataCommand -> Subtract VARIABLE_NAME From VARIABLE_NAME", lambda a, var1, t, var2: changeVarByVar(getValue(var2), var1, 'negate'))

		self.add_rule("DataCommand -> Multiply VARIABLE_NAME By NP", lambda m, var_name, b, np: setVariable(var_name, getProduct(getValue(var_name), np)))
		self.add_rule("DataCommand -> Multiply VARIABLE_NAME By VARIABLE_NAME", lambda m, var1, b, var2: setVariable(var1, getProduct(getValue(var1), getValue(var2))))

		self.add_rule("DataCommand -> Divide VARIABLE_NAME By NP", lambda d, var_name, b, np: setVariable(var_name, getQuotient(getValue(var_name), np)))
		self.add_rule("DataCommand -> Divide VARIABLE_NAME By VARIABLE_NAME", lambda d, var1, b, var2: setVariable(var1, getQuotient(getValue(var1), getValue(var2))))
		self.add_rule("DataCommand -> Change VARIABLE_NAME By NP", lambda c, var1, b, np: changeVarBy(getValue(var1), np))


		# todo: fix commands working w/ lists
		self.add_rule("Ele -> Det Ele", lambda d, e: e)
		self.add_rule("DataCommand -> Add ITEM To LIST_NAME", lambda a, item, t, list_name: addToList(list_name, item))
		self.add_rule("DataCommand -> Delete Ele NP Of LIST_NAME", lambda d, el, ind,o, list_name: deleteListItem(list_name,ind))
		self.add_rule("DataCommand -> Replace Ele NP Of LIST_NAME With ITEM", lambda r, e, ind, o, list_name,w, item: setItemInList(ind, list_name, item))
		self.add_rule("DataCommand -> Set Ele NP Of LIST_NAME To ITEM", lambda s, e, ind, o, list_name, t,item: setItemInList(ind, list_name, item))

		# Data Reporter
		self.add_rule("DataReporter -> The OrderAdverb Item In LIST_NAME", lambda t, order_adverb, i, inn, list_name: getItem(wordMap(order_adverb), list_name))

		# Number Phrase
		self.add_rule("NP -> Unk", lambda unk: getNumber(unk))
		self.add_rule("NP -> NPP", self.identity)
		self.add_rule("NP -> Det NPP", lambda det, npp: npp)
		self.add_rule("NP -> VARIABLE_NAME", lambda v: getValue(v))

		self.add_rule("NP -> NP Plus NP", lambda unk1, plus, unk2: add(unk1, unk2))
		self.add_rule("NP -> NP Added To NP", lambda unk1, added, to, unk2: add(unk1, unk2))
		self.add_rule("NPP -> Sum Of NP And NP", lambda s, of, unk1, a, unk2: add(unk1, unk2))

		self.add_rule("NP -> NP Minus NP", lambda unk1, minus, unk2: subtract(unk1, unk2))
		self.add_rule("NP -> NP Subtracted By NP", lambda unk1, subtracted, by, unk2: subtract(unk1,unk2))
		self.add_rule("NP -> NP Subtracted From NP", lambda unk1, subtracted, by, unk2: subtract(unk2,unk1))
		self.add_rule("NP -> Difference Between NP And NP", lambda d, b, n1, a, n2: subtract(n1,n2))

		self.add_rule("NP -> NP Times NP", lambda unk1, times, unk2: getProduct(unk1,unk2))
		self.add_rule("NP -> NP Multiplied By NP", lambda unk1, multiplied, by, unk2: getProduct(unk1,unk2))
		self.add_rule("NPP -> Product Of NP And NP", lambda product, of, unk1, a, unk2: getProduct(unk1,unk2))

		self.add_rule("NP -> NP Divided By NP", lambda unk1, divided, by, unk2: getQuotient(unk1,unk2))

		self.add_rule("NPP -> Random Number Between NP And NP", lambda r, n, b, unk1, a, unk2: getRandomNumberBetween(unk1, unk2))
		self.add_rule("NP -> Negative NP", lambda n, np: getProduct(-1,np))

		self.add_rule("Backdrop -> Det Backdrop", lambda d, b: b)
		self.add_rule("Backdrop -> Your Backdrop", lambda d, b: b)
		self.add_rule("Backdrop -> My Backdrop", lambda d, b: b)
		self.add_rule("BACKDROP_NAME -> Det BACKDROP_NAME", lambda d, b: b)
		self.add_rule("BACKDROP_NAME -> Backdrop Called BACKDROP_NAME", lambda d, c, b: b)
		self.add_rule("BACKDROP_NAME -> Backdrop Of BACKDROP_NAME", lambda d, c, b: b)

		self.add_rule("Program -> Det Program", lambda d, p: p)
		self.add_rule("Program -> My Program", lambda d, p: p)
		self.add_rule("Program -> Your Program", lambda d, p: p)

		self.add_rule("Timer -> Det Timer", lambda d, tim: [tim])
		self.add_rule("Timer -> My Timer", lambda d, tim: [tim])
		self.add_rule("Timer -> Your Timer", lambda d, tim: [tim])

		self.add_rule("Sprite -> Det Sprite", lambda d, s: s)
		self.add_rule("Sprite -> My Sprite", lambda d, s: s)
		self.add_rule("Sprite -> Your Sprite", lambda d, s: s)

		self.add_rule("EVENT -> When Det Green Flag Is Clicked", lambda w, t, g, f, i, c: whenGreenFlag())
		self.add_rule("EVENT -> When Green Flag Is Clicked", lambda w, g, f, i, c: whenGreenFlag())
		self.add_rule("EVENT -> When Program Starts", lambda w, p, s: whenGreenFlag())
		self.add_rule("EVENT -> When KEY_NAME Is Clicked", lambda w, name, iss, pressed: whenKeyClicked(name))
		self.add_rule("EVENT -> When Direction Is Clicked", lambda w, name, iss, pressed: whenKeyClicked(name + " arrow"))
		self.add_rule("EVENT -> When Sprite Is Clicked", lambda w, s, iss, cli: whenClicked())
		self.add_rule("EVENT -> When Backdrop Switches To BACKDROP_NAME", lambda w, b, s, t, name: whenBackSwitch(name))
		self.add_rule("EVENT -> When I Receive MESSAGE_NAME", lambda w, i, r, message: whenReceive(message))
		self.add_rule("EVENT -> When Timer CBP NP", lambda w, t, c, n: waitTillTimer(c([t], n)))

		self.add_rule("CBP -> CBP_equality", lambda i: i)
		self.add_rule("CBP_equality -> Equal To", lambda e, t: lambda a, b: equalTo(a,b))
		self.add_rule("CBP_equality -> Equals", lambda e: lambda a, b: equalTo(a,b))
		self.add_rule("CBP -> Greater Than", lambda g, t: lambda a, b: greaterThan(a, b))
		self.add_rule("CBP -> Less Than", lambda l, t: lambda a, b: lessThan(a, b))
		self.add_rule("CBP -> Greater Than Or Equal To", lambda g, t, o, e, too: lambda a, b: GEQ(a, b))
		self.add_rule("CBP -> Less Than Or Equal To", lambda l, t, o, e, too: lambda a, b: LEQ(a, b))

		self.add_rule("CBP -> LMOD CBP", lambda m, c: lambda a, b: m(c(a, b)))
		self.add_rule("CBP_equality -> LMOD CBP_equality", lambda m, eq: m(eq))

		self.add_rule("LMOD -> POS", lambda pos: lambda x: x)
		self.add_rule("LMOD -> NEG", lambda neg: lambda x: not_identity(x))

		self.add_rule("SimpleEventHandler -> EVENT AL ", lambda e, a: SimpleEvent(e, a))
		self.add_rule("EventHandler ->  SimpleEventHandler Thats It", lambda e, thats, it: e)
		self.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Thats It", lambda e, a, t, s, ti, thats, it: e)
		self.add_rule("EventHandler -> SimpleEventHandler Too Thats It", lambda e, t,thats, it: e)
		self.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Too Thats It", lambda e, a, t, s, ti, to, thats, it: e)

		## TimerCommand
		self.add_rule("TimerCommand -> Reset Timer", lambda r, t: resetTimer())

		## Boolean Phrases
		self.add_rule("Boolean -> TRUE" , lambda t: lambda x: x)
		self.add_rule("Boolean -> FALSE" , lambda t: lambda x: not_identity(x))
		self.add_rule("Boolean -> LMOD TRUE ", lambda l, t: lambda x: l(x))
		self.add_rule("Boolean -> LMOD FALSE" , lambda l, t: lambda x: l(not_identity(x)))

		self.add_rule("BP -> Ele NP In LIST_NAME", lambda i, unk, inn, name:itemInList(unk, name))
		self.add_rule("BP -> Ele NP LMOD In LIST_NAME", lambda i, unk, mod, inn, name: mod(itemInList(unk, name)))
		self.add_rule("BP -> LIST_NAME Contains ITEM", lambda name, con, it: itemInList(it, name))
		#self.add_rule("BP -> VARIABLE_NAME CBP NP", lambda var, cbp, unk: cbp(getValue(var), unk))
		self.add_rule("BP -> NP CBP NP", lambda unk1, cbp, unk2: cbp(unk1, unk2))
		self.add_rule("BP -> Timer CBP NP", lambda tim, comp, Unk: comp(tim, Unk))
		self.add_rule("BP -> VARIABLE_NAME CBP VARIABLE_NAME", lambda var1, cbp, var2: cbp(getValue(var1), getValue(var2)))

		self.add_rule("BP -> BP Boolean" , lambda b, boo: boo(b))
		self.add_rule("BP -> BP And BP", lambda b1,andd, b2: logicAnd(b1, b2))
		self.add_rule("BP -> BP Or BP", lambda b1, orr, b2: logicOr(b1, b2))
		self.add_rule("BP -> SBP", lambda sbp: sbp)

		## Comparison and Logic
		self.add_rule("CBP -> CBP_equality", lambda i: i)
		self.add_rule("CBP_equality -> Equal To", lambda e, t: lambda a, b: equalTo(a,b))
		self.add_rule("CBP_equality -> Equals", lambda e: lambda a, b: equalTo(a,b))
		self.add_rule("CBP -> Greater Than", lambda g, t: lambda a, b: greaterThan(a, b))
		self.add_rule("CBP -> Less Than", lambda l, t: lambda a, b: lessThan(a, b))
		self.add_rule("CBP -> Greater Than Or Equal To", lambda g, t, o, e, too: lambda a, b: GEQ(a, b))
		self.add_rule("CBP -> Less Than Or Equal To", lambda l, t, o, e, too: lambda a, b: LEQ(a, b))

		self.add_rule("CBP -> LMOD CBP", lambda m, c: lambda a, b: m(c(a, b)))
		self.add_rule("CBP_equality -> LMOD CBP_equality", lambda m, eq: m(eq))

		self.add_rule("LMOD -> POS", lambda pos: lambda x: x)
		self.add_rule("LMOD -> NEG", lambda neg: lambda x: not_identity(x))

		self.add_rule("SBP -> SP CBP_equality WP", lambda sp, eq, wp: equalTo(sp,wp)) # SBP = speech boolean phrase
		self.add_rule("SBP -> WP CBP_equality SP", lambda sp, eq, wp: equalTo(sp,wp))

		## Broadcast Commands
		self.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME", lambda broadcast, name: broadcastMessage(name))
		self.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME And Wait", lambda b, name, a, w: broadCastMessageWait(name))
		self.add_rule("MESSAGE_NAME -> Det MESSAGE_NAME", lambda d, name: name)
		self.add_rule("MESSAGE_NAME -> Message MESSAGE_NAME", lambda d, name: name)
		self.add_rule("Message -> New Message", lambda d, name: name)
		self.add_rule("Message -> Det Message", lambda d, name: name)
		self.add_rule("Message -> Message Called", lambda d, name: name)

		# Conditional Command
		self.add_rule("ConditionalCommand -> If BP Then AL Thats It", lambda i, bp, then, al, thats, it: ifCommand(bp,al))
		self.add_rule("ConditionalCommand -> If BP AL Thats It", lambda i, bp, al, thats, it: ifCommand(bp,al))
		self.add_rule("ConditionalCommand -> If BP Then AL Thats It Else AL Thats It", lambda i, bp, then, al1, thats1, it1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
		self.add_rule("ConditionalCommand -> If BP AL Thats It Else AL Thats It", lambda i, bp, al1, thats1, it1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
		self.add_rule("ConditionalCommand -> If BP Then AL Else AL Thats It", lambda i, bp, then, al1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
		self.add_rule("ConditionalCommand -> If BP AL Else AL Thats It", lambda i, bp, al1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))
		self.add_rule("ConditionalCommand -> If I Say WP Then AL Thats It", lambda i, me, s, wp, then, al, thats, it: [singleCommandNoValue("listenAndWait"), ifCommand(equalTo(singleCommandNoValue("getSpeech"),wp),al)])
		self.add_rule("ConditionalCommand -> If You Hear WP Then AL Thats It", lambda i, y, s, wp, then, al, thats, it: [singleCommandNoValue("listenAndWait"), ifCommand(equalTo(singleCommandNoValue("getSpeech"),wp),al)])

		# Control Command

		self.add_rule("ControlCommand -> Wait NP Seconds", lambda waitt, unk, seconds: wait(unk))
		self.add_rule("ControlCommand -> Wait Until BP", lambda wait, until, bp: waitUntil(bp))
		self.add_rule("ControlCommand -> Repeat AL Until BP", lambda repeat, al, untill, bp: until(bp, al))
		self.add_rule("ControlCommand -> Repeat AL Forever", lambda repeat, al, forever: doForever(al))
		self.add_rule("ControlCommand -> Repeat AL Unk Times", lambda repeatt, al, unk, times: repeat(unk, al))
		self.add_rule("ControlCommand -> Delete Det Clone", lambda delete, this, clone: deleteClone())

		#LoopCommand
		self.add_rule("LoopCommand -> Repeat LoopCommandP", lambda r, lcp: lcp)
		self.add_rule("LoopCommand -> LoopCommandP", self.identity)
		self.add_rule("LoopCommand -> AL Should Be Repeated Duration", lambda action_list, t,s,b,r, duration: repeat_action_list(action_list, duration))
		self.add_rule("LoopCommandP -> AP Duration", lambda ap, duration: repeat_action_list([ap], duration))
		self.add_rule("LoopCommandP -> The Following Duration AL Thats It", lambda t, f, duration, action_list, tt, i: repeat_action_list(action_list, duration))
		self.add_rule("LoopCommandP -> The Following Steps Duration AL Thats It", lambda t, f, s, duration, action_list, tt, i: repeat_action_list(action_list, duration))


		#General switches
		self.add_rule("To -> To Be", lambda t, b: t)



		#####################################################################
		## Lexicon

		## Determiners
		self.add_lexicon_rule("Det", ["the", "this", "a", "an"], lambda word: lambda: None)

		## Noun - pronouns
		self.add_lexicon_rule("I", ["i"], self.identity)
		self.add_lexicon_rule("You",["you"],self.identity)
		self.add_lexicon_rule("Your",["your"],self.identity)
		self.add_lexicon_rule("My",["my"],self.identity)
		self.add_lexicon_rule("Myself",["myself"],self.identity)
		self.add_lexicon_rule("It", ["it"], self.identity)

		## Noun - names
		self.add_lexicon_rule("NAME_OF_SOUND",
							 ["meow","cave","boing","chomp","drum","jungle","hey"],
							 # TODO: the semantic rule for NAME_OF_SOUND could involve
							 # searching
							 lambda name: name)
		self.add_lexicon_rule("LANGUAGE_NAME",
			["english", "danish", "dutch", "french", "german", "italian", "japanese", "russian"], lambda language: language.capitalize())
		self.add_lexicon_rule("VOICE_NAME", ["quinn", "max", "squeak", "giant", "kitten"], self.identity)
		self.add_lexicon_rule("Direction",["up", "left", "right", "down"],self.identity)
		self.add_rule("KEY_NAME -> Direction Arrow", lambda d, a: d+" "+a)

		self.add_lexicon_rule("Unk", ["0","1","2","3","4","5","6","7","8","9"], self.identity)
		self.add_lexicon_rule("SequenceAdverb", ["then", "after", "finally"], self.identity)

		self.add_lexicon_rule("DRUM", ["tambourine", "claves", "cowbell", "triangle", "bongo", "conga", "cabasa", "guiro", "vibraslap", "cuica"], self.identity)
		self.add_lexicon_rule("Drum1", ["snare", "bass", "side", "crash", "open", "closed", "hand", "wood"], self.identity)
		self.add_lexicon_rule("Drum2", ["drum", "stick", "cymbal", "highhat", "hi", "clap", "block"], self.identity)
		self.add_lexicon_rule("Drum3", ["hat"], self.identity)

		self.add_lexicon_rule("INSTRUMENT", ["piano", "organ", "guitar", "bass", "pizzicato", "cello", "trombone", "clarinet", "saxophone", "flute", "bassoon", "choir", "vibraphone", "marimba"], self.identity)
		self.add_lexicon_rule("Instrument1", ["electric", "wooden", "music", "steel", "synth"], self.identity)
		self.add_lexicon_rule("Instrument2", ["piano", "guitar", "flute", "box", "drum", "lead", "pad"], self.identity)


		self.add_lexicon_rule("OrderAdverb",
							   ["secondly", "fourthly", "fifthly", "seventh", "second", "fifth", "sixthly", "third", "thirdly", "fourth", "sixth", "firstly", "first"],
							   lambda word: wordMap(word))

		## Noun - keywords

		# Sounds
		self.add_lexicon_rule("Sounds", ["sounds"], self.identity)
		self.add_lexicon_rule("Sound", ["sound", "recording"], self.identity)
		self.add_lexicon_rule("Volume", ["volume"], self.identity)
		self.add_lexicon_rule("Pitch", ["pitch"], self.identity)
		self.add_lexicon_rule("Effect", ["effect"], self.identity)
		self.add_lexicon_rule("Percent", ["percent"], self.identity)
		self.add_lexicon_rule("Seconds", ["seconds","second"], self.identity)

		# Events
		self.add_lexicon_rule("Arrow",["arrow"],self.identity)
		self.add_lexicon_rule("Green", ["green"], self.identity)
		self.add_lexicon_rule("Flag", ["flag"], self.identity)
		self.add_lexicon_rule("Message",["message"],self.identity)
		self.add_lexicon_rule("Key",["key", "button"],self.identity)
		self.add_lexicon_rule("Program", ["program", "project"], self.identity)

		# Voice
		self.add_lexicon_rule("Response",["response", "reply"],self.identity)
		self.add_lexicon_rule("Speech",["speech"],self.identity)

		self.add_lexicon_rule("Voice",["voice"],self.identity)
		self.add_lexicon_rule("Language",["language"],self.identity)
		self.add_lexicon_rule("Accent",["accent"],self.identity)

		# Music
		self.add_lexicon_rule("Drum", ["drum", "instrument"], self.identity)
		self.add_lexicon_rule("Beats", ["beats", "beat"], self.identity)
		self.add_lexicon_rule("Note", ["note"], self.identity)
		self.add_lexicon_rule("Instrument", ["instrument"], self.identity)
		self.add_lexicon_rule("Tempo", ["tempo"], self.identity)
		self.add_lexicon_rule("Rest", ["rest"], self.identity)
		self.add_lexicon_rule("Per", ["per"], self.identity)
		self.add_lexicon_rule("Minute", ["minute"], self.identity)

		# Scratch specific
		self.add_lexicon_rule("Sprite", ["sprite"], self.identity)
		self.add_lexicon_rule("Sprites",["sprites"],self.identity)
		self.add_lexicon_rule("Backdrop", ["backdrop"], self.identity)
		self.add_lexicon_rule("Clone", ["clone"], self.identity)

		# data & variables
		self.add_lexicon_rule("List", ["list"], self.identity)
		self.add_lexicon_rule("Variable",["variable"],self.identity)

		## Verbs - Speech
		self.add_lexicon_rule("Listen",["listen"],self.identity)
		self.add_lexicon_rule("Hear",["hear"],self.identity)
		self.add_lexicon_rule("Say",["say", "voice", "speak"],self.identity) # TODO: is it safe to do map "Say" To "tell me", which has two words in it?
		self.add_lexicon_rule("Talk",["talk"],self.identity)


		## Keywords
		# Conditional Command Keywords
		self.add_lexicon_rule("If", ["if"], self.identity)
		self.add_lexicon_rule("Then", ["then"], self.identity)
		self.add_lexicon_rule("Else", ["else", "otherwise"], self.identity)
		self.add_lexicon_rule("Thats", ["thats"], self.identity)
		self.add_lexicon_rule("Until", ["until", "till"], self.identity)

		## Algebra Command Keywords
		self.add_lexicon_rule("Equals", ["equals", "is"], self.identity)
		self.add_lexicon_rule("Equal", ["equal"], self.identity)
		self.add_lexicon_rule("Greater", ["greater"], self.identity)
		self.add_lexicon_rule("Less", ["less"], self.identity)

		self.add_lexicon_rule("Divided",["divided"],self.identity)
		self.add_lexicon_rule("Divide",["divide"],self.identity)
		self.add_lexicon_rule("Multiply",["multiply"],self.identity)
		self.add_lexicon_rule("Multiplied",["multiplied"],self.identity)
		self.add_lexicon_rule("Times",["times"],self.identity)
		self.add_lexicon_rule("Product",["product"],self.identity)
		self.add_lexicon_rule("Minus",["minus"],self.identity)
		self.add_lexicon_rule("Subtracted",["subtracted"],self.identity)
		self.add_lexicon_rule("Difference",["difference"],self.identity)
		self.add_lexicon_rule("Sum",["sum"],self.identity)
		self.add_lexicon_rule("Added",["added"],self.identity)
		self.add_lexicon_rule("Plus",["plus"],self.identity)
		self.add_lexicon_rule("Negative",["negative", "minus"],self.identity)

		self.add_lexicon_rule("Random",["random", "a"],self.identity)
		self.add_lexicon_rule("Number",["number"],self.identity)

		# Data Command Keywords
		self.add_lexicon_rule("Log", ["log"], self.identity)
		self.add_lexicon_rule("Add", ["add", "append"], self.identity)
		self.add_lexicon_rule("Increment", ["increment", "increase"], self.identity)
		self.add_lexicon_rule("Decrement", ["decrement", "decrease"], self.identity)
		self.add_lexicon_rule("Subtract", ["subtract"], self.identity)
		self.add_lexicon_rule("Contains",["contains", "has"],self.identity)
		self.add_lexicon_rule("Called",["called", "named"],self.identity)
		self.add_lexicon_rule("Use", ["use"], self.identity)
		self.add_lexicon_rule("Set", ["set"], self.identity)
		self.add_lexicon_rule("Replace", ["replace"], self.identity)
		self.add_lexicon_rule("Change", ["change"], self.identity)
		self.add_lexicon_rule("Delete", ["delete"], self.identity)
		self.add_lexicon_rule("Ele",["element", "item"],self.identity)
		self.add_lexicon_rule("Make",["make", "create"],self.identity)

		# Loop Command Keywords
		self.add_lexicon_rule("Repeat", ["repeat", "do"], self.identity)
		self.add_lexicon_rule("Repeated", ["repeated", "done"], self.identity)
		self.add_lexicon_rule("Forever",["forever"],self.identity)
		self.add_lexicon_rule("Duration", ["forever"],self.identity)
		self.add_lexicon_rule("Steps", ["steps"], self.identity)
		self.add_lexicon_rule("Times", ["times"], self.identity)

		# Sound Command Keywords
		self.add_lexicon_rule("Softer",["softer", "quieter"],self.identity)
		self.add_lexicon_rule("Louder",["louder"],self.identity)
		self.add_lexicon_rule("Slower",["slower"],self.identity)
		self.add_lexicon_rule("Faster",["faster"],self.identity)
		self.add_lexicon_rule("Play", ["play"], self.identity)
		self.add_lexicon_rule("Stop", ["stop", "terminate"], self.identity)
		self.add_lexicon_rule("Wait", ["wait"], self.identity)
		self.add_lexicon_rule("SStart", ["start"], self.identity)

		# Logic Keywords
		self.add_lexicon_rule("Or", ["or"], self.identity)
		self.add_lexicon_rule("And", ["and"], self.identity)
		self.add_lexicon_rule("NEG", ["not"], self.identity)
		self.add_lexicon_rule("NEG", ["isnt"], self.identity)# not working
		self.add_lexicon_rule("POS", ["is"], self.identity)
		self.add_lexicon_rule("TRUE", ["true"], self.identity)
		self.add_lexicon_rule("FALSE", ["false"], self.identity)
		self.add_rule("NEG -> Is NEG", lambda x, y: y)

		# Event Keywords
		self.add_lexicon_rule("When", ["when"], self.identity)
		self.add_lexicon_rule("Whenever",["whenever", "when"],self.identity)
		self.add_lexicon_rule("Clicked", ["pressed", "clicked"], self.identity)
		self.add_lexicon_rule("Starts", ["starts"], self.identity)
		self.add_lexicon_rule("Switches", ["switches"], self.identity)
		self.add_lexicon_rule("Receive", ["receive"], self.identity)
		self.add_lexicon_rule("Broadcast",["broadcast"],self.identity)

		# Timer Keywords
		self.add_lexicon_rule("Timer", ["timer"], self.identity)
		self.add_lexicon_rule("Reset", ["reset", "zero", "restart", "initialize"], self.identity)

		## Adj
		self.add_lexicon_rule("All",["all"],self.identity)
		self.add_lexicon_rule("Following",["following"],self.identity)
		self.add_lexicon_rule("Same", ["same"], self.identity)
		self.add_lexicon_rule("New",["new"],self.identity)
		self.add_lexicon_rule("Every",["every", "each"],self.identity)
		self.add_lexicon_rule("Single",["single"],self.identity)
		self.add_lexicon_rule("Time", ["time"], self.identity)

		## Other random words
		self.add_lexicon_rule("Should", ["should"], self.identity)
		self.add_lexicon_rule("Too", ["too", "simultaneously"], self.identity)
		self.add_lexicon_rule("Between",["between"],self.identity)
		self.add_lexicon_rule("From",["from"],self.identity)
		self.add_lexicon_rule("With",["with"],self.identity)
		self.add_lexicon_rule("Than", ["than"], self.identity)
		self.add_lexicon_rule("Is", ["is"], self.identity)
		self.add_lexicon_rule("At", ["at"], self.identity)
		self.add_lexicon_rule("In", ["in"], self.identity)
		self.add_lexicon_rule("For", ["for"],self.identity)
		self.add_lexicon_rule("Of", ["of", "from"],self.identity)
		self.add_lexicon_rule("That", ["that"], self.identity)
		self.add_lexicon_rule("Be", ["be"], self.identity)
		self.add_lexicon_rule("The", ["the"], self.identity)
		self.add_lexicon_rule("This", ["this"], self.identity)
		self.add_lexicon_rule("To",["to"],self.identity)
		self.add_lexicon_rule("By",["by"],self.identity)
		self.add_lexicon_rule("As",["as"],self.identity)

