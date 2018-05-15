import os
from zipfile import ZipFile
import sys

raw_project_path = '/Users/quacht/Downloads/generate_sb2_fixture_with_assets'

if len(sys.argv) > 1:
	raw_project_path = sys.argv[0]
zipfile_path = raw_project_path + '.zip'
sb2_path = raw_project_path + '.sb2'
os.system('zip -r ' + zipfile_path + ' ' + raw_project_path)
os.system('mv ' + zipfile_path + ' ' + sb2_path)
