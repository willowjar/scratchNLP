import sqlite
from flask import g
import uuid
import sys
from scratch_project import ScratchProject

DATABASE = 'database.db'

def get_db():
	db = getattr(g, '_database', None)

	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	# db.row_factory = sqlite3.Row

	return db

# @app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

# Given a ScratchProject object, we either update an existing project entry or
# create a new entry into the database
def insert_into_db(project):
	db = get_db()
	cur = db.cursor()
	author_id = project.author
	created = project.created
	project_name = project.name;
	instructions = str(project.instructions)
	project_json = project.to_json()
	cur.execute("INSERT INTO projects (author_id,project_name,instructions,json) VALUES (?,?,?,?)", (author_id,project_name,instructions,project_json))
	db.commit()

def update(project):
	db = get_db()
	cur = db.cursor()
	author_id = project.author
	created = project.created
	project_name = project.name;
	instructions = str(project.instructions)
	project_json = project.to_json()
	cur.execute("REPLACE INTO projects (author_id,project_name,instructions,json) VALUES (?,?,?,?)", (author_id,project_name,instructions,project_json))
	db.commit()
	return "Updated project"

# When I get a project, in what format do I want it
def get_project(project_name, author_id):
	scratch_project = None
	db = get_db()
	project = query_db('select * from projects where project_name = ? and author_id = ?',
				[project_name, author_id], one=True)
	if project:
		# Create a ScratchObject from the representation stored in the database.
		print("This is what the database query returns to me")
		scratch_project = ScratchProject(project)
	return scratch_project
