
import semanticRules

# CodiSemanticRuleSet is a class that wraps the SemanticRuleSet
# class so that every rule set will correspond to a specific project
# with its own variables, lists, and sounds.
class CodiSemanticRuleSet:
	def __init__(self):
		self.variables = {}
		self.lists = {}
		self.sounds = set()
		self.sem = SemanticRuleSet()

# Redefine semantic rules that depend on global variables, lists, and sounds.


####################################################################
# Actions that use variables, lists, and sounds.

def refresh_project_specific_rules(sem):

	def soundToNumber(string):
		sounds = {"snare drum": 1, "bass drum": 2, "side stick": 3, "crash cymbal": 4, "open hi hat": 5, "open highhat": 5, "closed hi hat": 6, "closed highhat": 6, "tambourine": 7, "hand clap": 8, "claves": 9, "wood block": 10, "cowbell": 11, "triangle": 12, "bongo": 13, "conga": 14, "cabasa": 15, "guiro": 16, "vibraslap": 17, "cuica": 18}
		if string in sounds:
			# Add the sound to the project.
			global_sounds.add(string)
			# Return the number corresponding to desired sound.
			return sounds[string]
		else:
			## TODO RAISE ERROR
			return 1

	def playInstrumentBeats(sound, beats):
		# Add the sound to the project.
		global_sounds.add(sound)
		return ["playDrum", sound, beats]

	def rest(numberOfBeats):
		return ['rest:elapsed:from:', numberOfBeats]

	def InstrumentToNumber(string):
		sounds = {"piano": 1, "electric piano": 2, "organ": 3, "guitar": 4, "electric guitar": 5, "bass": 6, "pizzicato": 7, "cello": 8, "trombone": 9, "clarinet": 10, "saxophone": 11, "flute": 12, "wooden flute": 13, "bassoon": 14, "choir": 15, "vibraphone": 16, "music box": 17, "steel drum": 18, "marimba": 18, "synth lead": 20, "synth pad": 21}
		if string in sounds:
			# Add the sound to the project.
			global_sounds.add(string.title())
			return sounds[string]
		else:
			## TODO RAISE ERROR
			return 0

	# Speech Actions
	def processSentence(data):
		if len(data) > 0:
			data = [thing for thing in data if thing != None]
			return {'scripts': data, 'variables': global_variables, 'lists': global_lists, 'sounds': global_sounds}

	def playSound(name):
		# Add the sound to the project.
		global_sounds.add(name.title())
		return ["doPlaySoundAndWait", name.title()]

	def startSound(name):
		# Add the sound to the project.
		global_sounds.add(name.title())
		return ["playSound:", name.title()]

	def logVariable(var_name):
		if (var_name in global_variables):
			whatToSay = var_name + " is " + str(getValue(var_name))
		else:
			whatToSay = "You don't have a variable called " + var_name
		return ["speakAndWait:", whatToSay]

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

	# Rules depending on the things above.

	sem.add_rule('MusicCommand -> Play DRUM For NP Beats' , lambda p, i, f, n, b: playInstrumentBeats(soundToNumber(i), n))
	sem.add_rule('MusicCommand -> Play DRUM NP Beats' , lambda p, i, n, b: playInstrumentBeats(soundToNumber(i), n))
	sem.add_rule('MusicCommand -> Rest For NP Beats' , lambda r, f, numberOfBeats, b: rest(numberOfBeats))
	sem.add_rule('MusicCommand -> Use INSTRUMENT', lambda u, i: setInstrument(InstrumentToNumber(i)))
	sem.add_rule('MusicCommand -> Set Instrument To INSTRUMENT', lambda s, i, t, ii: setInstrument(InstrumentToNumber(ii)))
	sem.add_rule('MusicCommand -> Set Det Instrument To INSTRUMENT', lambda s, d, i, t, ii: setInstrument(InstrumentToNumber(ii)))
	sem.add_rule('MusicCommand -> Use INSTRUMENT As Det Instrument', lambda u, ii, a, d, i: setInstrument(InstrumentToNumber(ii)))
	sem.add_rule('MusicCommand -> Play INSTRUMENT', lambda p, i: setInstrument(InstrumentToNumber(i)))
	sem.add_rule("Start -> S", lambda s: processSentence(s))
	sem.add_rule("SoundCommand -> SStart NAME_OF_SOUND", lambda start, name: startSound(name))
	sem.add_rule("SoundCommand -> Play NAME_OF_SOUND", lambda play, name: playSound(name))
	sem.add_rule("DataCommand -> Log VARIABLE_NAME", lambda log, var_name: logVariable(var_name))
	sem.add_rule("DataCommand -> Delete VARIABLE_NAME", lambda delete, var_name: deleteVariable(var_name))
	sem.add_rule("CreateCommand -> Make VARIABLE_LIST", lambda make, vl: createVariable(vl))

