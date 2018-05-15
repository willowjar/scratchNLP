import json
import os
import zipfile
from scratch_project_base import ScratchProjectBase

class ScratchProject(ScratchProjectBase):
	def __init__(self):
		ScratchProjectBase.__init__(self)
		self.variables = {}
		self.lists = {}
		self.stacks = []
		self.scripts = []

	def add_variable(self,name, opt_value = 0):
		"""Create a variable initialized to 0"""
		#if opt_value:
		self.variables[name] = opt_value
		#else:
				#if name in self.variables:
					#raise Exception('A variable called ' + name + 'has already been created')
				#self.variables[name] = 0


	def add_list(self, name, opt_contents):
		"""Create a list initialized to 0"""
		print('add lists')
		if opt_contents:
			self.lists[name] = opt_contents
		else:
			#if name in self.lists:
					#raise Exception('A list called ' + name + 'has already been created')
			self.lists[name] = []

	def add_script(self, script):
		# TODO: verify is this correct behavior
		if (script):
			if (script[0][0].startswith('when')):
				# detected an event block
				# create a stack of old scripts
				if len(self.scripts) > 0:
					self.add_stack(self.scripts)
				# create a new stack for event handler
				self.add_stack(script)
			else:	
				self.scripts.append(script)

	def add_stack(self, script_list):
		stack = [5,128] + [script_list]
		self.stacks.append(stack)

	def to_json(self):
		# TODO: return and verify the json of the entire project
		# not just the first/only sprite
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

		sprite1["scripts"] = self.stacks
		self.json["children"][0] = sprite1
		return json.dumps(self.json)

	def save_project(self, path_to_project_directory):
		# write the project.json into a file
		with open(os.path.join(path_to_project_directory, 'project.json'), 'w+') as f:
			f.write(self.to_json())
		# zip and rename the file
		
