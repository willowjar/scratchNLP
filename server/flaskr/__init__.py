import os
import sys
from flask import Flask
import db
import time
sys.path.insert(0,'../scripts/')
from semantic import process_instruction, process_single_instruction
from scratch_project import ScratchProject

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize the database
    db.init_db(app)

    # TODO(quacht): This corresponds to a POST if it's the first instruction.
    # if it's not, it's a PUT.
    # Create or update a specific project with an instruction
    @app.route('/user/<user_name>/project/<project_name>/script/<raw_instruction>')
    def process(user_name, project_name, raw_instruction):
        database = db.get_db()
        project =  db.query_db('select * from projects where project_name = ?',
                [project_name], one=True)
        if project is None:
            # No such project exists, create a new one
            project = ScratchProject();
            project.name = project_name
            project.instructions = [raw_instruction]
            project.author = "tina"
            db.insert_into_db(project)
            return 'No such project, created new project, and tried to insert it'
        else:
            # Update entry  for the projects
            db.update_project(project, raw_instruction)
            return 'Updated project'
        # load current project into ScratchProject object
        result = process_instruction(raw_instruction, scratch_project)
        # TODO: update database with updated project
        # Return the new script to the client
        # return process_instruction(raw_instruction, scratch_project)
        # return 'project: {projectName}, instruction: {instruction}'.format(projectName=project_name, instruction=raw_instruction)

    # TODO(quacht): This corresponds to a GET
    @app.route('/user/<user_name>/project/<project_name>')
    def get_project(project_name):
        database = db.get_db()
        user = {'id':'tina'}
        project =  db.query_db('select * from projects where project_name = ?',
                [project_name], one=True)
        if project is None:
            # No such project exists, create a new one
            return 'No such project'
        else:
            # print project (1, u'tina', u'2018-06-27 03:56:37', u'tellmeajoke', u'sayyo')
            return str(project)

    # TODO(quacht): This corresponds to a GET. Consider only returning
    # projects that are public.
    # This should return all projects stored in the database
    @app.route('/allprojects')
    def get_all_projects():
        database = db.get_db()
        user = {'id':'tina'}
        projects = db.query_db('select * from projects')
        if len(projects) == 0:
            return 'No projects'

        return str(projects)

    @app.route('/user/<user_name>/allprojects')
    def get_all_projects_by(user):
        database = db.get_db()
        projects = db.query_db('select * from projects where author_id = ?', [project_name])
        if len(projects) == 0:
            return 'No projects'

        return str(projects)

    # TODO(quacht): This corresponds to a GET.
    @app.route('/translate/<instruction>')
    def translate(instruction):
        result = process_single_instruction(instruction)
        return str(result)

    return app