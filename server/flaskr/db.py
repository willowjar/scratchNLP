import sqlite3
from flask import g
import uuid

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

def insert_into_db(project):
    # TODO make sure this and udpate match the schema
    db = get_db()
    cur = db.cursor()
    author_id = project.author
    created = project.created
    project_name = project.name;
    instructions = str(project.instructions);
    # created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    # project_name TEXT NOT NULL,
    # instructions TEXT NOT NULL,
    # variables TEXT,
    # lists TEXT,
    # stacks TEXT,
    # scripts TEXT,
    cur.execute("INSERT INTO projects (author_id,project_name,instructions) VALUES (?,?,?)", (author_id,project_name,instructions))
    db.commit()

def update_project(project, raw_instruction):
    project_name = project[3]
    author_id = project[1]

    db = get_db()
    cur = db.cursor()
    instructions = project[4] + '\n' + raw_instruction

    cur.execute("INSERT OR REPLACE INTO projects (author_id,project_name,instructions) VALUES (?,?,?)", (author_id,project_name,instructions))
    db.commit()
