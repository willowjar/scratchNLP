#!/usr/bin/env python

from websocket_server import WebsocketServer
import json

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
	messageObject = json.loads(message)
	server.send_message_to_all(json.dumps({"id":messageObject["id"], "response":"echo echo"}));

PORT=8765
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
