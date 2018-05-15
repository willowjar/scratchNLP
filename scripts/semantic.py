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
from nltk.tree import Tree
from nltk.draw.tree import TreeView

import semanticRules as lab_rules
import generate_vocab as gv
from scratch_project import ScratchProject

sys.path.insert(0,'../../software/')
import lab3
from lab3.drawtree import TreeView as MultiTreeView
from lab3.production_matcher import decorate_parse_tree
from lab3.lambda_interpreter import eval_tree, decorate_tree_with_trace
from lab3.semantic_rule_set import SemanticRuleSet

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


def parse_input_str(input_str, scratch):
	# Before attempting to parse the sentence, update the grammar.
	gv.add_unknowns_to_grammar(input_str, lab_rules.sem, scratch)
	trees = lab_rules.sem.parse_sentence(input_str)
	if len(trees) > 1:
		print_verbose("[WARNING] Obtained %d parses; selecting the first one."%(len(trees)))
	elif len(trees) == 0:
		raise Exception("Failed to parse the sentence: " + input_str)
	return trees[0]


def handle_syntax_parser_mode(tree, sem_rule_set):
	#print "Parse Tree: "
	#print tree
	if args.gui:
		TreeView(decorate_parse_tree(tree,
									 sem_rule_set,
									 set_productions_to_labels=True))


def validate_output(actual_output, expected_output):
	if actual_output == expected_output:
		print "[VALIDATION] SUCCESS: '%s' does match expected output: '%s'"%(actual_output, expected_output)
	else:
		print "[VALIDATION] FAILURE: '%s' does not match expected output: '%s'"%(actual_output, expected_output)


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


def run_repl(sem_rule_set, batch_sentences=[], valid_output=[]):
	assert isinstance(sem_rule_set, SemanticRuleSet)
	batch_mode = len(batch_sentences) != 0
	output_validation_mode = len(valid_output) != 0

	scratch = ScratchProject()
	
	evaluation_history = []
	while True:
		# Read in a sentence.
		input_str = read_sentence(batch_sentences if batch_mode else None)
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
			path_to_result = '/afs/athena.mit.edu/course/6/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/result/'
			print scratch.save_project(path_to_result)
			continue

		# Parse the sentence.
		output = None
		try:
			tree = parse_input_str(input_str, scratch)
			if args.spm:
				handle_syntax_parser_mode(tree, sem_rule_set)
				continue
			else:
				# Evaluate the parse tree.
				decorated_tree = decorate_parse_tree(tree,
													 sem_rule_set,
													 set_productions_to_labels=False)
				trace = eval_tree(decorated_tree,
								  sem_rule_set,
								  args.verbose)
				evaluation_history.append(deepcopy(trace))
				output = trace[-1]['expr']

				# process output to update scratch project
				for x in output["variables"]:
					scratch.add_variable(x, output["variables"][x])
				for x in output["lists"]:
					scratch.add_list(x, output["lists"][x])

				for script in output["scripts"]:
					scratch.add_script(script)

				if args.gui:
					display_trace_gui(decorate_parse_tree(deepcopy(tree),
														  sem_rule_set,
														  set_productions_to_labels=True),
									  sem_rule_set)

		except Exception as e:
			# The parser did not return any parse trees.
			print_verbose("[WARNING] Could not parse input.")
			traceback.print_exc() # Uncomment this line while debugging.
			output = "I don't understand."

		# Print the result of the speech act
		print output

		if output_validation_mode:
			validate_output(output, valid_output[0])
			del valid_output[0]

		if args.show_database:
			lab_rules.sem.learned.print_knowledge()


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
	# my_rules.add_my_rules(lab_rules.sem)

	# Start the Semantics REPL.
	run_repl(lab_rules.sem,
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


