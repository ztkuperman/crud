import os
import sys

import flask
from flask import session, request
from flask_session import Session
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import crud.data.db_session as db_session
import crud.oso.oso_auth as oso_auth


app = flask.Flask(__name__)

def main():
    configure()
    app.run(debug=True, port=5006)


def configure():
    print("Configuring Flask app:")
    register_blueprints()
    print("Registered blueprints.")

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
    # Configuration for flask-session
    app.config['SESSION_KEY_PREFIX'] = "CRUD"
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_FILE_DIR'] = os.path.join(
                                    os.path.dirname(__file__), 'cache')
    Session(app)
    print("Configured Session.")

    oso_auth.init_oso()
    print("Configured Oso.")

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
    from crud.views import user_views
    from crud.views import editor_views
    from crud.views import auth_views

    app.register_blueprint(read_views.blueprint)
    app.register_blueprint(update_views.blueprint)
    app.register_blueprint(user_views.blueprint)
    app.register_blueprint(editor_views.blueprint)
    app.register_blueprint(auth_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
