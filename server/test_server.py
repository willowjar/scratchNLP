# file overview: Test the ScratchNLP API
import requests
import unittest
import urllib

# api-endpoint for the flask app
URL = "http://127.0.0.1:5000/"

class TestScratchNLPAPI(unittest.TestCase):
	# # TODO: fix so that test passes and then enable test.
 #  #   def test_add_instruction(self):
	# 	# # sending get request and saving the response as response object
	# 	# testcases = [{
	# 	# 'user_name': 'tina',
	# 	# 'project_name': 'hi',
	# 	# 'raw_instruction': 'say hello',
	# 	# 'response': 'No such project, created new project, and tried to insert it'
	# 	# }, {
	# 	# 'user_name': 'tina',
	# 	# 'project_name': 'hi',
	# 	# 'raw_instruction': "say who's there",
	# 	# 'response': 'Updated project '
	# 	# }]

	# 	# for testcase in testcases:
	# 	# 	url = URL + "user/%s/project/%s/script/%s" %(urllib.quote_plus(testcase['user_name']), urllib.quote_plus(testcase['project_name']), urllib.quote_plus(testcase['raw_instruction']))
	# 	# 	r = requests.get(url = url)
	# 	# 	data = r.text
	# 	# 	self.assertEqual(data, testcase['response'])

	# def test_add_instruction_to_project(self):
	# 	user_name = "tina"
	# 	project_name = "show me your inner cat"
	# 	raw_instruction = "play the meow sound 5 times"

	# 	url = URL + "user/%s/project/%s/script/%s" %(user_name, project_name, raw_instruction)
	# 	print(url)
	# 	r = requests.get(url = url)
	# 	data = r.text
	# 	print("data")
	# 	print(data)
	# 	self.assertEqual(str(data), "play the meow sound")

	# def test_translate_instruction(self):
	# 	# sending get request and saving the response as response object
	# 	testcases = [
	# 	# TODO(quacht): support the say command.
	# 	# {
	# 	# 'raw_instruction': 'say hello',
	# 	# 'response': 'No such project, created new project, and tried to insert it'
	# 	# },
	# 	# {
	# 	# 'raw_instruction': "say who's there",
	# 	# 'response': 'Updated project '
	# 	# },
	# 	# {
	# 	# 'raw_instruction': 'if x is not less than three then broadcast hello thats it',
	# 	# 'response': str([['doIf', ['not', ['<', ['readVariable', 'x'], 3]], [['broadcast:', 'hello']]]])
	# 	# },
	# 	{
	# 	'raw_instruction': "play the meow sound 10 times",
	# 	'response': str([['doRepeat', 10, [['doPlaySoundAndWait', 'meow']]]])
	# 	}]

	# 	for testcase in testcases:
	# 		url = URL + "translate/%s" %(testcase['raw_instruction'])
	# 		r = requests.get(url = url)
	# 		data = r.text
	# 		self.assertEqual(str(data), testcase['response'])


	# def test_get_project(self):
	# 	self.assertTrue(True)

	# def test_get_all_projects(self):
	# 	self.assertTrue(True)

	def test_get_scratch_program(self):
		project_name = "let's dance"
		payload = {'instructions': ['play the meow sound', 'play the chomp sound 10 times'],
            'useGreenFlag': True,
            'start': 0,
            'end': 1}
		url = URL + "scratch_program/%s" %(project_name)
		print(url)
		r = requests.post(url = url, data=payload)
		print(r.text)
		self.assertEquals(r.text, "")

if __name__ == '__main__':
	unittest.main()