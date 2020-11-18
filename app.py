import os
import sys

import flask
from flask import session
from flask_session import Session

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
import crud.data.db_session as db_session

app = flask.Flask(__name__)

SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), 'cache')


def main():
    configure()
    Session(app)
    app.run(debug=True, port=5006)


def configure():
    print("Configuring Flask app:")
    SECRET_KEY = os.urandom(32)
    register_blueprints()
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_FILE_DIR'] = os.path.join(
                                    os.path.dirname(__file__), 'cache')

    print("Registered blueprints")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'crud.sqlite')

    db_session.global_init(db_file)


def register_blueprints():
    from crud.views import read_views
    from crud.views import update_views
    from crud.views import editor_views
    from crud.views import auth_views

    app.register_blueprint(read_views.blueprint)
    app.register_blueprint(update_views.blueprint)
    app.register_blueprint(editor_views.blueprint)
    app.register_blueprint(auth_views.blueprint)

if __name__ == '__main__':
    main()
else:
    configure()
