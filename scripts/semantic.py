#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
6.863 - Spring 2018 - semantic.py
"""

from copy import deepcopy
import argparse
import readline
import traceback
import sys
import json
import os

from semanticRules import CodiSemanticRuleSet
import generate_vocab as gv
sys.path.insert(0,'../server/flaskr')
from scratch_project import ScratchProject

sys.path.insert(0,'../../software/')
from nltk.tree import Tree
from nltk.draw.tree import TreeView
import lab3
from lab3.drawtree import TreeView as MultiTreeView
from lab3.production_matcher import decorate_parse_tree
from lab3.lambda_interpreter import eval_tree, decorate_tree_with_trace
from lab3.semantic_rule_set import SemanticRuleSet

##############################################################################
# Initialize args in case we are not running this script as the main script.
class MockArgs:
	def __init__(self):
		self.verbose = None
		self.gui = None
		self.spm = None
global args
args = MockArgs()

# set lab rules
default_semantic_rules = CodiSemanticRuleSet()
##############################################################################

def print_verbose(s):
	if args.verbose:
		print s


def read_sentence(batch_mode_sentences=None):
	if batch_mode_sentences != None:
		if len(batch_mode_sentences) == 0:
			return None
		else:
			input_str = batch_mode_sentences[0]
			del batch_mode_sentences[0]
			print "> " + input_str
			return input_str
	else:
		try:
			return str(raw_input("> ")).strip()
		except ValueError:
			print "[ERROR] Invalid input. (could not parse as a string)"
			return None
		except EOFError:
			return ""
		except KeyboardInterrupt:
			return ""

# TODO: add some sort of metric for discriminating between parses
#  This metric could be doing it by simplest parse?
def parse_input_str(semantic_rule_set, input_str,opt_scratch_project=None):
	# Before attempting to parse the sentence, update the grammar.
	gv.add_unknowns_to_grammar(input_str, semantic_rule_set, opt_scratch_project)
	trees = semantic_rule_set.parse_sentence(input_str)
	index_of_tree_to_pick = 0
	if len(trees) > 1:
		print("[WARNING] Obtained %d parses; selecting the parse with the largest height."%(len(trees)))
		tree_heights= [tree.height() for tree in trees]
		index_of_tree_to_pick = tree_heights.index(min(tree_heights))
	elif len(trees) == 0:
		raise Exception("Failed to parse the sentence: " + input_str)

	assert("I don't understand." != trees[0])
	return trees[index_of_tree_to_pick]


def handle_syntax_parser_mode(tree, sem_rule_set):
	#print "Parse Tree: "
	#print tree
	if args.gui:
		TreeView(decorate_parse_tree(tree,
									 sem_rule_set,
									 set_productions_to_labels=True))


def validate_output(actual_output, expected_output):
	# The output returned by our system is a dictionary, not a string...
	# convert to a string before comparing.
	if str(actual_output) == expected_output:
		# print "[VALIDATION] SUCCESS: '%s' does match expected output: '%s'"%(actual_output, expected_output)
		pass
	else:
		# print "[VALIDATION] FAILURE: '%s' does not match expected output: '%s'"%(actual_output, expected_output)
		print "[VALIDATION] FAILURE:"
		print "expected: '%s'" %(expected_output)
		print "got: '%s'" %(actual_output)

def display_trace_gui(GUI_decorated_tree, sem_rule_set):
	# Display the GUI of the trace through the evaluation.
	if args.gui:
		try:
			trace_to_display = eval_tree(GUI_decorated_tree, sem_rule_set, verbose=False)
			tv = MultiTreeView([decorate_tree_with_trace(entry['tree']) for entry in trace_to_display])
			tv.update()
			tv.showTree()
		except:
			traceback.print_exc()

##############################################################################
def process_single_instruction(semantic_rule_set, input_str, opt_scripts_only=False):
	"""
	Given an input string process the string to generate the appropriate
	Scratch scripts. The script gets added the the ScratchProject object
	"""
	# Ideally, we would only generate the vocabulary list once...
	gv.generate_vocab_list(semantic_rule_set)

	# tina look here
	batch_sentences=[]
	valid_output=[]

	# Parse the sentence.
	output = None
	try:
		tree = parse_input_str(semantic_rule_set, input_str)
		if args.spm:
			handle_syntax_parser_mode(tree, semantic_rule_set)
			# continue
		else:
			# print('PRODUCTIONS IN SEMANTIC BEFORE DECORATING')
			# print(semantic_rule_set.productions)
			# Evaluate the parse tree.
			decorated_tree = decorate_parse_tree(tree,
												 semantic_rule_set,
												 set_productions_to_labels=False)
			trace = eval_tree(decorated_tree,
							  semantic_rule_set,
							  args.verbose)

			output = trace[-1]['expr']

			if args.gui:
				display_trace_gui(decorate_parse_tree(deepcopy(tree),
													  semantic_rule_set,
													  set_productions_to_labels=True),
								  semantic_rule_set)

	except Exception as e:
		# The parser did not return any parse trees.
		# print_verbose("[WARNING] Could not parse input.")
		traceback.print_exc() #TODO: Uncomment this line while debugging.
		return "I don't understand."
		# output = e

	if opt_scripts_only:
		# Return only the bracketed representation
		return output['scripts']
	# Return the dictionary representing the changes to make to the Scratch
	# Project
	return output

def run_repl(semantic_rule_set, batch_sentences=[], valid_output=[]):
	assert isinstance(semantic_rule_set, SemanticRuleSet)
	batch_mode = len(batch_sentences) != 0
	output_validation_mode = len(valid_output) != 0

	scratch = ScratchProject()
	gv.generate_vocab_list(semantic_rule_set)

	evaluation_history = []
	while True:
		# Read in a sentence.
		input_str = read_sentence(batch_sentences if batch_mode else None)
		if not input_str:
			break
		input_str = input_str.lower().strip()
		if input_str in ('', 'exit', 'quit'):
			if batch_mode:
				# We ignore these special commands in batch mode.
				continue
			else:
				# Exit the REPL.
				break
		# you should be able to use the repl to query the value of lists and
		# variables if they exist.
		elif input_str == None:
			if batch_mode:
				break
			else:
				continue
		elif input_str in scratch.variables:
			print scratch.variables[input_str]
			continue
		elif input_str in scratch.lists:
			print scratch.lists[input_str]
			continue
		elif input_str == 'json':
			print scratch.to_json()
			continue
		elif input_str == 'make scratch project' or input_str in 'make sb2':
			# path_to_result = '/afs/athena.mit.edu/course/6/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/result/'
			path_to_result = '../../BuiltProjects/'
			print scratch.save_project(path_to_result)
			continue

		# Parse the sentence.
		changes = process_single_instruction(semantic_rule_set, input_str)
		if changes != "I don't understand.":
			scratch.update(changes)

			if args.gui:
				display_trace_gui(decorate_parse_tree(deepcopy(tree),
													  semantic_rule_set,
													  set_productions_to_labels=True),
								  semantic_rule_set)
		if changes == "I don't understand.":
			# The parser did not return any parse trees.
			print_verbose("[WARNING] Could not parse input.")
			traceback.print_exc() #TODO: Uncomment this line while debugging.

		# Print the result of the speech act
		print changes

		if output_validation_mode:
			validate_output(changes, valid_output[0])
			del valid_output[0]

		if args.show_database:
			semantic_rule_set.learned.print_knowledge()


##############################################################################


def parse_cli_args():
	arg_parser = argparse.ArgumentParser(description='6.863 - Spring 2018 - Semantics Interpreter')
	arg_parser.add_argument('-v',
							'--verbose',
							action='store_true',
							help='output evaluation traces.')
	arg_parser.add_argument('--spm',
							action='store_true',
							help='syntax parser mode (no semantic evaluation).')
	arg_parser.add_argument('--gui',
							action='store_true',
							help="""
								 display a graphical user interface for stepping
								 through the trace of the last evaluation prior to
								 the exiting of the program
								 """)
	arg_parser.add_argument('--batch_mode',
							dest='batch_file',
							type=str,
							required=False,
							help='evaluate each sentence listed in the specified file')
	arg_parser.add_argument('--show_database',
							action='store_true',
							help='display the contents of the semantic database after each evaluation')
	arg_parser.add_argument('--validate_output',
							dest='validation_file',
							type=str,
							required=False,
							help='check the specified input against expected output.')
	return arg_parser.parse_args()


def main():
	print "> Loading the 6.863 Semantics REPL..."

	batch_sentences=[]
	if args.batch_file != None:
		try:
			print "> Running in batch mode. Reading sentences from: " + args.batch_file
			# Read in the list of sentences.
			with open(args.batch_file, 'r') as f_bm:
				batch_sentences = [x.strip() for x in f_bm]
		except IOError as e:
			print "[ERROR] Could not open the file: %s"%(args.batch_file)
			return
	else:
		print "> Hello. To exit this program, enter <cr> at the prompt below."

	# If validating output, read in the expected output.
	valid_output = []
	if args.validation_file != None:
		if args.batch_file == None:
			print "[ERROR] Must be in batch mode to validate output."
			return
		elif args.spm:
			print "[ERROR] Cannot validate output in syntax parser mode."
			return
		try:
			print "> Validating output against " + args.validation_file
			with open(args.validation_file, 'r') as f_vo:
				valid_output = [x.strip() for x in f_vo]
				assert len(batch_sentences) == len(valid_output)
		except IOError as e:
			print "[ERROR] Could not open the file: %s"%(args.validation_file)

	# import my_rules
	# my_rules.add_my_rules(default_semantic_rules)

	# Start the Semantics REPL.
	run_repl(default_semantic_rules,
			 batch_sentences=batch_sentences,
			 valid_output=valid_output)

	# Exit the program.
	print "> Goodbye."


if __name__=='__main__':
	# if len(sys.argv) > 1:
	# 	path_to_base_project_dir = sys.argv[1]
	# 	path_to_result = sys.argv[2]
	# else:
	#default path to base_project_dir
	args = parse_cli_args()
	main()


