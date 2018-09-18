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

    # This corresponds to a POST if it's the first instruction. If it's not, it
    # is a PUT. However, in actual use of the system, the client makes a get
    # request to the following URL (route) which then gets serviced by this code
    @app.route('/user/<user_name>/project/<project_name>/script/<raw_instruction>')
    def process(user_name, project_name, raw_instruction):
        # Create or update a specific project with an instruction
        database = db.get_db()

        project =  db.query_db('select * from projects where project_name = ?',
                [project_name], one=True)
        if project is None:
            # No such project exists, create a new one
            project = ScratchProject();
            project.name = project_name
            project.instructions = [raw_instruction]
            project.author = user_name
            db.insert_into_db(project)
            return "Inserted project into db"
        else:
            # TODO: properly read in the project object
            project_object = ScratchProject(project)
            # update the project_object appropriately...
            opt_full_json = True
            changes_to_add = process_single_instruction(raw_instruction, opt_full_json)
            project_object.update(changes_to_add)
            # Update entry  for the projects
            db.update(project_object)
            return 'Updated project'

        # After updating the project, send the appropriate project state back to
        # client.
        return get_project(project_name)

    # TODO(quacht): This corresponds to a GET
    @app.route('/user/<user_name>/project/<project_name>')
    def get_project(user_name, project_name):
        database = db.get_db()
        project =  db.get_project(project_name, user_name)
        if project is None:
            # No such project exists, create a new one
            return 'No such project'
        else:
            # TODO: Rather than returning only the json that represents the project as expected by
            # the scratch parser, how should we handle the information corresponding
            # to the metadata of the project.
            return str(project.to_json())

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
    def get_all_projects_by(user_name):
        database = db.get_db()
        projects = db.query_db('select * from projects where author_id = ?', [user_name])
        # if len(projects) == 0:
        #     return 'No projects'

        return str(projects)

    # TODO(quacht): This corresponds to a GET.
    @app.route('/translate/<instruction>')
    def translate(instruction):
        result = process_single_instruction(instruction)
        return str(result)

    return app