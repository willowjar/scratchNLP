#!/usr/bin/env python

# https://github.com/Pithikos/python-websocket-server
from websocket_server import WebsocketServer
import json

import os
import sys
import time

sys.path.insert(0,'../../scripts/')
from semanticRules import CodiSemanticRuleSet
from semantic import process_single_instruction
from scratch_project import ScratchProject

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all(json.dumps({"message":"Hey all, a new client has joined us"}))

# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, server, message):
	print("Client(%d) said: %s" % (client['id'], message))

	# The message contains information about the request sent from scratch-vui
	message_json = json.loads(message)
	if "type" in message_json:
		if message_json["type"] == "translation":
			handle_request_for_translation(client, message_json)
		if message_json["type"] == "project":
			handle_request_for_project(client, message_json)
	else:
		server.send_message(client, json.dumps({"id":message_json["id"], "response":"echo"}));
	print("")

def handle_request_for_translation(client, message_json):
	translation = process_single_instruction(CodiSemanticRuleSet(), message_json["instruction"], False)

	# Send translation to client
	message = json.dumps({"id":message_json["id"], "response": str(translation)})
	server.send_message(client, message)

def handle_request_for_project(client, message_json):
	user_name = message_json["user"]
	project_name = message_json["projectName"]

	# Force the request to get its contents as JSON so that we actually
	# get the payload of the request instead of None.
	info = message_json
	instruction_list = info['instructions']
	use_green_flag = info['useGreenFlag']

	if ('start' in info and 'end' in info):
		start = info['start']
		end = info['end']
		instructions = instruction_list[int(start):int(end)]
	else:
		instructions = instruction_list

	# TODO: determine whether this project is shared across multiple connections?
	project = ScratchProject()
	project.author = user_name
	semantic_rule_set = CodiSemanticRuleSet()
	for instruction in instructions:
		changes_to_add = process_single_instruction(semantic_rule_set, instruction)
		print("changes_to_add when creating a new project:")
		print(changes_to_add)
		if changes_to_add != "I don't understand.":
			# The instruction was valid and parseable.
			project.update(changes_to_add)
		else:
			# Oh no! One of the instructions in the project was invalid!
			# TODO: generate a block that communicates what the invalid instruction was at that part of the project,
			# that way, when the project executes, the user will know. Still, we hope that no invalid instructions will ever get
			# put into the project.
			# TODO: consider also returing an array or sequence of invalid instructions and their locations.
			pass

	print(client["id"], project)
	message = json.dumps({"id":message_json["id"], "response": project.to_json(use_green_flag)})
	server.send_message(client, message)

PORT=8765
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
