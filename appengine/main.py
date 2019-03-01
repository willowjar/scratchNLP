# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

from flask import Flask, request
from flask_cors import CORS, cross_origin

import os
import sys
import db
import time

# sys.path.insert(0,'../../scripts/')
# from semantic import process_single_instruction
# from scratch_project import ScratchProject

# # Create and configure the app
app = Flask(__name__, instance_relative_config=True)
# # Enable Cross-Origin Resource Sharing (CORS), meaning other domains
# # can make requests that will be handled by our API.
CORS(app)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# # ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass

# # initialize the database
# db.init_db(app)

# # This corresponds to a POST if it's the first instruction. If it's not, it
# # is a PUT. However, in actual use of the system, the client makes a get
# # request to the following URL (route) which then gets serviced by this code
# @app.route('/user/<user_name>/project/<project_name>/script/<raw_instruction>')
# def process(user_name, project_name, raw_instruction):
#      # "Inserted project into db" or 'Updated project'
#     print(_update_project(user_name, project_name, raw_instruction))

#     # After updating the project, send the appropriate project state back to
#     # client.
#     return get_project(user_name, project_name)

# def _update_project(user_name, project_name, raw_instruction):
#     '''Args:
#         project_name - name of project as stored in database
#         raw_instruction - the text representation of what the user said'''
#     # Create or update a specific project with an instruction
#     database = db.get_db()

#     project =  db.query_db('select * from projects where project_name = ? and author_id = ?',
#             [project_name, user_name], one=True)

#     if project is None:
#         # No such project exists, create a new one
#         project = ScratchProject();
#         project.name = project_name
#         project.instructions = [raw_instruction]
#         project.author = user_name
#         changes_to_add = process_single_instruction(raw_instruction)
#         project.update(changes_to_add)
#         db.insert_into_db(project)
#         return "Inserted project into db"
#     else:
#         # TODO: properly read in the project object
#         project_object = ScratchProject(project)
#         # update the project_object appropriately...
#         changes_to_add = process_single_instruction(raw_instruction)
#         project_object.update(changes_to_add)
#         # Update entry  for the projects
#         db.update(project_object)
#         return 'Updated project'

# @app.route('/user/<user_name>/project/<project_name>')
# def get_project(user_name, project_name):
#     database = db.get_db()
#     project =  db.get_project(project_name, user_name)
#     if project is None:
#         # No such project exists, create a new one
#         return 'No such project'
#     else:
#         # TODO: Rather than returning only the json that represents the project as expected by
#         # the scratch parser, how should we handle the information corresponding
#         # to the metadata of the project.
#         return str(project.to_json())

# # TODO(quacht): Consider only returning
# # projects that are public.
# # This should return all projects stored in the database
# @app.route('/allprojects')
# def get_all_projects():
#     database = db.get_db()
#     user = {'id':'tina'}
#     projects = db.query_db('select * from projects')
#     if len(projects) == 0:
#         return 'No projects'

#     return str(projects)

# @app.route('/user/<user_name>/allprojects')
# def get_all_projects_by(user_name):
#     database = db.get_db()
#     projects = db.query_db('select * from projects where author_id = ?', [user_name])
#     # if len(projects) == 0:
#     #     return 'No projects'

#     return str(projects)

# @app.route('/translate/<instruction>')
# @cross_origin()
# def translate(instruction):
#     result = process_single_instruction(instruction, False)
#     return str(result)

# # Get the project json for the user and project. If the use green flag
# # option is set to true, then
# def _get_project_helper(user_name, project_name, opt_use_green_flag=False):
#     database = db.get_db()
#     project =  db.get_project(project_name, user_name)
#     if project is None:
#         # No such project exists, create a new one
#         return 'No such project'
#     else:
#         return str(project.to_json(opt_use_green_flag))

# @app.route('/user/<user_name>/scratch_program/<project_name>', methods=["POST"])
# @cross_origin(allow_headers=['Content-Type'], methods=["POST"], send_wildcard=True)
# def generate_project_without_store(user_name, project_name):
#     if request.method =="POST":
#         print("get json")
#         # Force the request to get its contents as JSON so that we actually
#         # get the payload of the request instead of None.
#         info = request.get_json(force=True)
#         instruction_list = info['instructions']
#         use_green_flag = info['useGreenFlag']

#         if ('start' in info and 'end' in info):
#             start = info['start']
#             end = info['end']
#             instructions = instruction_list[int(start):int(end)]
#         else:
#             instructions = instruction_list

#         project = ScratchProject();
#         project.author = user_name
#         for instruction in instructions:
#             changes_to_add = process_single_instruction(instruction)
#             print("changes_to_add when creating a new project:")
#             print(changes_to_add)
#             if changes_to_add != "I don't understand.":
#                 # The instruction was valid and parseable.
#                 project.update(changes_to_add)
#             else:
#                 # Oh no! One of the instructions in the project was invalid!
#                 # TODO: generate a block that communicates what the invalid instruction was at that part of the project,
#                 # that way, when the project executes, the user will know. Still, we hope that no invalid instructions will ever get
#                 # put into the project.
#                 # TODO: consider also returing an array or sequence of invalid instructions and their locations.
#                 pass
#         return str(project.to_json(use_green_flag))

@app.route('/')
def hello():
    return 'Hi tina hello World!'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]