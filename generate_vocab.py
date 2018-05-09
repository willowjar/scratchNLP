#!/usr/bin/python
import re
from text2num import text2int

# TODO(quacht): add argument validation
# TODO(quacht): specify which vocabulary file to append generate rules to.


# Use regex to match specific Scratch commands and do simple error
# checking to validate arguments
expressionMap = {
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

numberExpressionMap = {
	r'subtract (.*) from (.*)': ['NUMBER','NUMBER'],
	r'(.*) subtracted by (.*)': ['NUMBER','NUMBER'],
	r'(.*) minus (.*)': ['NUMBER','NUMBER'],
	r'divide (.*) by (.*)': ['NUMBER','NUMBER'],
	r'multiply (.*) by (.*)': ['NUMBER','NUMBER'],
	r'(.*) divided by (.*)': ['NUMBER','NUMBER'],
	r'(.*) times (.*)': ['NUMBER','NUMBER'],
	r'a random number between (.*) and (.*)': ['NUMBER','NUMBER'],
	r'(.*) add (.*)': ['NUMBER','NUMBER'],
	r'add (.*) to (.*)': ['NUMBER','NUMBER']
 }

def extractVocab(expressionMapList, sentences):
	result = {}
	for sentence in sentences:
		for expressionMap in expressionMapList:
			for expression in expressionMap:
				regex = expression[0]
				variables = expression[1]
				matchObj = re.match(regex, sentence, re.M|re.I)
				if matchObj:
					for i in range(1, len(variables)+1):
						if variables[i-1] in result:
							result[variables[i-1]].add(matchObj.group(i));
						else:
							result[variables[i-1]] = set([matchObj.group(i)])
	return result

# Read sentences to extract variable and list names.
example_sentences_file = "example_sentences.text"
with open(example_sentences_file) as f:
    content = f.readlines()
sentences = [x.strip() for x in content]

expressionMapList = [expressionMap, numberExpressionMap]
new_vocab = extractVocab(expressionMapList, sentences)

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

# Given a vocab dictionary and vocabulary file, generate the vocab.
def add_to_vocabulary_file(vocab, vocabulary_file):
	with open(vocabulary_file, "a+") as myfile:
		for key in vocab:
			print(key)
			print(vocab[key])
			for instance in vocab[key]:
				myfile.write(key + " -> " + instance + "\n")

vocabulary_file = "new_vocab_file.txt"
add_to_vocabulary_file(new_vocab, vocabulary_file)


