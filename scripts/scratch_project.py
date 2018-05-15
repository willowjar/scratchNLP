import json
import os
from zipfile import ZipFile
import sys
import json
from scratch_project_base import ScratchProjectBase

class ScratchProject(ScratchProjectBase):
	def __init__(self):
		ScratchProjectBase.__init__(self)
		self.variables = {}
		self.lists = {}
		self.stacks = []
		self.scripts = []
		self.project_dir_path = ''


	def add_variable(self,name, opt_value=0):
		"""Create a variable initialized to 0"""
		self.variables[name] = opt_value


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

	def save_project(self, path_to_output_dir):
		raw_project_path = '/afs/athena.mit.edu/course/6/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/test_fixtures/generate_sb2_fixture_with_assets'
		# write the project.json into a file
		with open(os.path.join(raw_project_path, 'project.json'), 'w+') as f:
			f.write(self.to_json())
		# zip and rename the file
		project_name = 'scratchNLPdemo'
		current_dir = os.getcwd()
		os.chdir(raw_project_path)

		zipfile_path = os.path.join(raw_project_path, project_name + '.zip')
		os.system('zip -r ' + zipfile_path + ' ./*')

		sb2_path = os.path.join(path_to_output_dir, project_name + '.sb2')
		print('sb2_path is ' + sb2_path)

		os.system('mv ' + zipfile_path + ' ' + sb2_path)
		os.chdir(current_dir)