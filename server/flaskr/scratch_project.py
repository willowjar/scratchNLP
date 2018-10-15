import os
from zipfile import ZipFile
import sys
import json
import time
from scratch_project_base import ScratchProjectBase
import copy

class ScratchProject(ScratchProjectBase):
	def __init__(self, opt_db_info=None):
		ScratchProjectBase.__init__(self)
		# project state
		self.variables = {}
		self.lists = {}
		self.stacks = []
		self.scripts = []
		self.project_dir_path = ''
		# db information
		if opt_db_info:
			self.load_from_db(opt_db_info)
		else:
			self.created = time.time()
			self.name = None
			self.author = None
			self.instructions = None
			self.id = None

	def load_from_db(self, db_tuple):
		self.id = db_tuple[0]
		self.author = db_tuple[1]
		self.created = db_tuple[2]
		self.name = db_tuple[3]
		self.instructions = db_tuple[4]
		self.json = json.loads(db_tuple[5])

	def update(self, changes):
		"""Given changes to add, update representation of the Scratch Project."""
		for x in changes["variables"]:
			self.add_variable(x, changes["variables"][x])
		for x in changes["lists"]:
			self.add_list(x, changes["lists"][x])
		# remove any variables or lists that were deleted.
		for var in self.variables:
			if var not in changes["variables"]:
				del self.variables[var]
		for var in self.lists:
			if var not in changes["lists"]:
				del self.lists[var]

		for script in changes["scripts"]:
			self.add_script(script)

	def add_variable(self,name, opt_value=0):
		"""Create a variable initialized to 0"""
		self.variables[name] = opt_value

	def add_to_list(self, name, element):
		self.lists[name].append(element)

	def add_list(self, name, opt_contents=[]):
		"""Create a list initialized to empty list"""
		self.lists[name] = opt_contents

	def add_script(self, script):
		# TODO: verify is this correct behavior
		if len(script) > 0 and script[0] != None and script != None:
			if (script[0][0].startswith('when')):
				# detected an event block
				# create a stack of old scripts
				if len(self.scripts) > 0:
					self.add_stack(self.scripts)
					self.scripts = []
				# create a new stack for event handler
				self.add_stack(script)
			else:
				self.scripts.append(script)

	def add_stack(self, script_list):
		stack = [5,128] + [script_list]
		self.stacks.append(stack)

	def _copy_with_green_flag(self, scratch_project_dict):
		new_dict = copy.deepcopy(scratch_project_dict)
		sprite1 = new_dict["children"][0]
		for i in range(0,len(sprite1["scripts"])):
			stack = sprite1["scripts"][i]
			# If the stack doesn't already begin with an event hat block, then
			# add the when green flag clicked event hat block to it so that
			# the instructions will be executed when the project starts.
			program_nested_array = stack[2]
			if len(program_nested_array) > 0:
				print("program_nested_array[0]")
				print(program_nested_array[0])
				if not program_nested_array[0][0].startswith("when"):
					sprite1["scripts"][i][2] = [["whenGreenFlag"]] + program_nested_array
		return new_dict

	def to_json(self, opt_use_green_flag=False):
		sprite1 = self.json["children"][0]
		sprite1["variables"] = []
		for key, value in self.variables.items():
			sprite1["variables"].append({
					"name": key,
					"value": value,
				})
		sprite1["lists"] = []
		for key, value in self.lists.items():
			sprite1["lists"].append({
					"listName": key,
					"contents": value,
				})
		# Include current scripts in the json
		self.add_stack(self.scripts)
		sprite1["scripts"] = self.stacks
		self.json["children"][0] = sprite1

		# The current scripts should not ACTUALLY be included in
		# stacks until the current script stacks have been completed
		# or a new stack is started.
		self.stacks = self.stacks[:-1]

		dict_representation = self.json
		if opt_use_green_flag:
			# All stacks that do not already use an event, should begin with a green flag?
			dict_representation = self._copy_with_green_flag(self.json)
		return json.dumps(dict_representation)

	def save_project(self, path_to_output_dir):
		# raw_project_path = '/afs/athena.mit.edu/course/6/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/test_fixtures/generate_sb2_fixture_with_assets'
		raw_project_path = '../test_fixtures/generate_sb2_fixture_with_assets'
		# write the project.json into a file
		with open(os.path.join(raw_project_path, 'project.json'), 'w+') as f:
			f.write(self.to_json())
		# zip and rename the file
		project_name = 'scratchNLPdemo'
		current_dir = os.getcwd()

		os.chdir(raw_project_path)
		curdir = os.getcwd()
		zipfile_path = os.path.join(curdir, project_name + '.zip')

		os.system('zip -r ' + zipfile_path + ' ./*')
		print("** zip path", zipfile_path)

		# if path the specified output directory doesn't exist yet, create the
		# folder accordingly.
		if not os.path.exists(path_to_output_dir):
				os.makedirs(path_to_output_dir)
		print(curdir, path_to_output_dir)
		sb2_path = os.path.join(path_to_output_dir, project_name + '.sb2')
		print('sb2_path is ' + sb2_path)

		os.system('mv ' + zipfile_path + ' ' + sb2_path)
		os.chdir(current_dir)

