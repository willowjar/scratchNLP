#!/usr/bin/python
import sys
import re
from text2num import text2int

# Reference explaining the regexs seen in the expression map.
# It's useful to test a regular expression using https://pythex.org/
regexMap = {
	'single word': r'(\w*)',
	'phrase': r'((?:\w+\s)+)',
	'anything': r'(?:.*)'
}

# Use regex to match specific Scratch commands and do simple error
# checking to validate arguments
# global
expression_map = {
  r'message called (\w*)': ['MESSAGE_NAME'],
  r'variable called (\w*)': ['VARIABLE_NAME'],
  r'variable named (\w*)': ['VARIABLE_NAME'],
  r'list called (\w*)': ['LIST_NAME'],
  r'list named (\w*)': ['LIST_NAME'],
  r'item (\w*) is in list (\w*)': ['ITEM', 'LIST_NAME'],
  r'(\w*) contains (\w*)': ['LIST_NAME', 'ITEM'],
  r'play the (\w*) sound': ['NAME_OF_SOUND'],
  #r'play the ((?:\w+\s)+?)sound': ['NAME_OF_SOUND'],
  r'wait (\w*) seconds': ['Unk'],
  r'broadcast (\w*)': ['MESSAGE_NAME'],
  r'when I receive (\w*)': ['MESSAGE_NAME'],
  r'set (\w*) to .*': ['VARIABLE_NAME'],
  r'add (\w*) to list (\w*)': ['ITEM','LIST_NAME'],
  r'item (\w*) is in list (\w*)': ['ITEM', 'LIST_NAME'],
}

speech_command_map = {
  r'(?:say|speak|voice) ((?:\w|\s)*)': ['WP'], # Word Phrase
  r'set voice to (\w*)': ['VOICE_NAME'],
  r'set accent to (\w*)': ['LANGUAGE_NAME'],
  r'(?:when|if|whenever) you hear ((?:\w|\s)*) say ((?:\w|\s)*)': ['WP', 'WP'], # Concern: would need to generate this regex for every command, replacing "say". Maybe a good workaround is to map every "unknown to a word."
  r'(?:when|if|whenever) i say ((?:\w|\s)*) say ((?:\w|\s)*)': ['WP', 'WP'],
  r'the speech (?:is|equals|is equal to) ((?:\w|\s)*)': ['WP'],
  r'((?:\w|\s)*) (?:is|equals|is equal to) the speech': ['WP'],
}
# global
expression_map_list = [expression_map, speech_command_map]

def add_item_to_dict(key_value_tuple, dictionary):
	key = key_value_tuple[0]
	value =key_value_tuple[1]
	if key in dictionary:
		dictionary[key].add(value)
	else:
		dictionary[key] = set([value])
	# print('add_item_to_dict')
	# print('\tdictionary[key]: ' + str(dictionary[key]))

def extract_names_and_words(sentences):
	""" Use the the global expression map list to extract variable, list, and
	message names and also words contained in phrases.
	Args:
		sentences (array of str): sentences from which to extract vocabulary
	Returns:
		dict: map of each nonterminal to a list of terminals.
	"""
	result = {}

	for sentence in sentences:
		for expression_map in expression_map_list:
			for regex in expression_map:
				variables = expression_map[regex]
				matches = re.findall(regex, sentence, re.M|re.I) #  re.M (multi-line), re.I (ignore case)

				if len(variables) == 1:
					this_variable = variables[0]
					matches_set = set(matches)
					for match in matches_set:
						# Word phrases need to be split before they are included in the
						# grammar through semantic rules
						if this_variable == "WP":
							for word in match.strip().split():
								add_item_to_dict(('Word', word), result)
						else:
							add_item_to_dict((this_variable, match.strip()), result)
				else:
					#assume results grouped by tuple if there are atleast 1 result
					for i in range(0, len(variables)):
						this_variable = variables[i]
						if len(matches)> 0 and i < len(matches):
							matches_for_this_var = matches[i]
							for match in matches_for_this_var:
								if this_variable == "WP":
									for word in match.strip().split():
										add_item_to_dict(('Word', word), result)
								else:
									add_item_to_dict((this_variable, match.strip()), result)
	# print('extract_names_and_words:')
	# print('\tsentence: ' + str(sentences))
	# print('\tresult: ' + str(result))
	return result

def add_to_vocabulary_file(vocab, vocabulary_file, opt_append=None):
	"""
	Given a vocab dictionary and vocabulary file, generate the vocab and put it
	into the given file.

	Args:
		vocab (dict): dictionary that maps each nonterminal to a list of
			terminals.
		vocabulary_file (str): path to vocab file
		opt_append (str|boolean): whether or not to append to the vocabulary file

	"""
	mode = "w+"
	if opt_append:
		mode="a+"
	with open(vocabulary_file, mode) as myfile:
		for key in vocab:
			for instance in vocab[key]:
				myfile.write("1\t" + key + "\t" + instance + "\n")
	myfile.close()

def add_to_lexicon(vocab, semantic_rule_set):
	"""
	Given a vocab dictionary and vocabulary file, generate the vocab and put it
	into the given file.

	Args:
		vocab (dict): dictionary that maps each nonterminal to a list of
			terminals.
	"""
	for key in vocab:
		semantic_rule_set.add_lexicon_rule(key, vocab[key], lambda word: word)


def get_core_vocab():
	new_vocab = {}

	# Define the kinds of keys that may be pressed and responded to.
	keynames = ['space','any']
	# Include all lowercase letters
	keynames = keynames + [chr(letter) for letter in range(97,123)]
	# Include all digits
	keynames = keynames + [str(num) for num in range(0,10)]
	new_vocab['KEY_NAME'] = keynames

	# Include same numbers digits
	new_vocab['Unk'] = [str(num) for num in range(0,10)]

	# Add the names of Scratch backdrops.
	backdrops = ['Party','Basketball', 'Jurassic', 'Light', 'Rays', 'Refrigerator', 'Space']
	new_vocab['BACKDROP_NAME'] = backdrops

	return new_vocab

def generate_vocab_list(semantic_rule_set):
	new_vocab = get_core_vocab()
	add_to_lexicon(new_vocab, semantic_rule_set)

def generate_vocab_list_with_examples(example_sentences_file_path, vocabulary_file_path):
	with open(example_sentences_file_path) as f:
		content = f.readlines()
	sentences = [x.strip() for x in content]

	new_vocab = extract_names_and_words(sentences)
	core_vocab = get_core_vocab()

	final_vocab = core_vocab.copy()
	final_vocab.update(new_vocab)

	add_to_vocabulary_file(final_vocab, vocabulary_file)

def replace_unknowns(utterance, grammar_file_path):
	""" Get list of unknown words and the utterance with all unknowns replaced
	with 'Unk'

	Args:
		utterance (str): the user's speech

	Returns:
		(str, list of strings): a tuple containing the new utterance and
			the unknown words
	"""
	with open(grammar_file_path) as f:
		content = f.read() + '\n'

	pattern = re.compile(r'1\tUnk\t(.*)')
	logged_unknowns = set(re.findall(pattern, content))

	# Known words must come from the right hand side of rules
	pattern = re.compile(r'(?: |\t)(.*)')
	flatten = lambda l: [item for sublist in l for item in sublist]
	known_words = set(flatten([phrase.split() for phrase in re.findall(pattern, content)]))

	utterance_tokens = utterance.split()

	unk_list = []
	new_utterance = []
	for word in utterance_tokens:
		if word not in known_words or word in logged_unknowns:
			# replace
			new_utterance.append('Unk')
			if word not in logged_unknowns:
				unk_list.append(word)
		else:
			# keep
			new_utterance.append(word)

	new_utterance = ' '.join(new_utterance)
	return (new_utterance, unk_list)

def get_unknowns_given_productions(utterance, semantic_rule_set):
	""" Get list of unknown words

	Args:
		utterance (str): the user's speech
		semantic_rule_set (SemanticRuleSet): the object containing the rules

	Returns:
		(str, list of strings): a tuple containing the new utterance and
			the unknown words
	"""
	logged_unknowns = [production.rhs() for production in semantic_rule_set.productions if production.lhs() == 'Unk']

	# Known words must come from the right hand side of rules
	known_right_hand_sides = [production.rhs() for production in semantic_rule_set.productions]
	flatten = lambda l: [item for sublist in l for item in sublist]
	known_words = flatten(known_right_hand_sides)
	utterance_tokens = utterance.split()

	unk_list = []
	for word in utterance_tokens:
		if word not in known_words or word in logged_unknowns:
			if word not in logged_unknowns:
				unk_list.append(word)

	return unk_list

def add_unknowns_to_grammar(utterance, semantic_rule_set, opt_scratch_project=None):
	""" All words that do not yet exist in the grammar or vocabulary must be
	added to the vocabulary.
	Args:
		utterance (str): The utterance in which to find unknowns.
		grammar_file_path (str): The path to the grammar file.
	Returns:
		str: the utterance with the unknowns replaced with 'Unk'
	"""

	# Add unknown names from utterance to the grammar
	utterance_vocab = extract_names_and_words([utterance])
	if opt_scratch_project:
		# Add variables to the scratch project object.
		if 'VARIABLE_NAME' in utterance_vocab:
			for var in utterance_vocab['VARIABLE_NAME']:
				opt_scratch_project.add_variable(var)

	# Add the names to the syntactic/semantic rules
	add_to_lexicon(utterance_vocab, semantic_rule_set)
	# Find all unknown words in the input, save them in the grammar, and replace
	#  them with 'Unk' which represents that they are unknown.
	unk_list = get_unknowns_given_productions(utterance, semantic_rule_set)

	vocab_map = {
		'Unk': unk_list,
		}

	add_to_lexicon(vocab_map, semantic_rule_set)

def add_unknowns_to_grammar_file(utterance, grammar_file_path):
	""" All words that do not yet exist in the grammar or vocabulary must be
	added to the vocabulary.
	Args:
		utterance (str): The utterance in which to find unknowns.
		grammar_file_path (str): The path to the grammar file.
	Returns:
		str: the utterance with the unknowns replaced with 'Unk'
	"""
	# Add unknown names from utterance to the grammar
	utterance_vocab = extract_names_and_words([utterance])
	add_to_vocabulary_file(utterance_vocab, grammar_file_path, 'append')

	# Find all unknown words in the input, save them in the grammar, and replace
	#  them with 'Unk' which represents that they are unknown.
	new_utterance, unk_list = replace_unknowns(utterance, grammar_file_path)

	vocab_map = {'Unk': unk_list}
	add_to_vocabulary_file(vocab_map, grammar_file_path, 'append')
	return new_utterance

if __name__ == "__main__":
	pass
