#!/usr/bin/python
import sys
import re
from text2num import text2int

# TODO(quacht): add argument validation
# TODO(quacht): specify which vocabulary file to append generate rules to.


# Use regex to match specific Scratch commands and do simple error
# checking to validate arguments
# global
expression_map = {
  r'message called (.*)': ['MESSAGE_NAME'],
  r'variable called (.*)': ['VARIABLE_NAME'],
  r'list called (.*) for': ['LIST_NAME'],
  r'item (.*) is in list (.*)': ['ITEM', 'LIST_NAME'],
  r'(.*) contains (.*)': ['LIST_NAME', 'ITEM'],
  r'play the (.*) sound': ['NAME_OF_SOUND'],
  r'wait (.*) seconds': ['NUMBER'],
  r'broadcast (.*)': ['MESSAGE_NAME'],
  r'when I receive (.*)': ['MESSAGE_NAME'],
  r'delete variable (.*)': ['VARIABLE_NAME'],
  r'set (.*) to .*': ['VARIABLE_NAME'],
  r'change (.*) by .*': ['VARIABLE_NAME'],
  r'make a list called (.*) for': ['LIST_NAME'],
  r'add (.*) to list (.*)': ['ITEM','LIST_NAME'],
  r'delete element .* of list (.*)': ['LIST_NAME'],
  r'replace element .* of list (.*) with .*': ['LIST_NAME'],
  r'the first item in list (.*)': ['LIST_NAME'],
}

# global
expression_map_list = [expression_map]

def extract_names(sentences):
	""" Use the the global expression map list to extract variable, list, and
	message names
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
				matchObj = re.match(regex, sentence, re.M|re.I)
				if matchObj and matchObj.group():
					for i in range(1, len(variables)+1):
						print regex
						print variables[i-1]
						print matchObj.group(i)
						print ''
						if variables[i-1] in result:
							result[variables[i-1]].add(matchObj.group(i));
						else:
							result[variables[i-1]] = set([matchObj.group(i)])
	return result

def add_to_vocabulary_file(vocab, vocabulary_file, opt_append):
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

def generate_vocab_list(example_sentences_file_path, vocabulary_file_path):
	with open(example_sentences_file_path) as f:
		content = f.readlines()
	sentences = [x.strip() for x in content]

	new_vocab = extract_names(sentences)

	# Define the kinds of keys that may be pressed and responded to.
	keynames = ['space','left arrow', 'right arrow', 'down arrow', 'up arrow', 'any']
	# Include all lowercase letters
	keynames = keynames + [chr(letter) for letter in range(97,123)]
	# Include all digits
	keynames = keynames + [str(num) for num in range(0,10)]
	new_vocab['KEY_NAME'] = keynames

	# Add the names of Scratch backdrops.
	backdrops = ['Party','Basketball', 'Blue Sky', 'Blue Sky 2', 'Jurassic', 'Light', 'Rays', 'Refrigerator', 'Space']
	new_vocab['BACKDROP_NAME'] = backdrops

	add_to_vocabulary_file(new_vocab, vocabulary_file)

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

	pattern = re.compile(r'1	Unk	(.*)')
	logged_unknowns = set(re.findall(pattern, content))

	# Known words must come from the right hand side of rules
	pattern = re.compile(r' (.*)')
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

def add_unknowns_to_grammar(utterance, grammar_file_path):
	""" All words that do not yet exist in the grammar or vocabulary must be
	added to the vocabulary.
	Args:
		utterance (str): The utterance in which to find unknowns.
		grammar_file_path (str): The path to the grammar file.
	Returns:
		str: the utterance with the unknowns replaced with 'Unk'
	"""

	# Add unknown names from utterance to the grammar
	utterance_vocab = extract_names([utterance])
	print utterance_vocab
	add_to_vocabulary_file(utterance_vocab, grammar_file_path, 'append')

	# Find all unknown words in the input, save them in the grammar, and replace
	#  them with 'Unk' which represents that they are unknown.
	new_utterance, unk_list = replace_unknowns(utterance, grammar_file_path)
	vocab_map = {'Unk': unk_list}
	add_to_vocabulary_file(vocab_map, grammar_file_path, 'append')
	return new_utterance

if __name__ == "__main__":
	if len(sys.argv) == 3:
		vocabulary_file = sys.argv[1]
		example_sentences_file = sys.argv[2]

		# Read sentences to extract variable and list names.
		example_sentences_file = "example_sentences.text"
		vocabulary_file = "new_vocab_file.txt"

		# Generate vocab file
		generate_vocab_list(example_sentences_file, vocabulary_file)
	else:
		print('Usage: generate_vocab.py <vocabulary_file_path> <example_sentences>')

