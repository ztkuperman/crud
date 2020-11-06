import os
import sys

import flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
import crud.data.db_session as db_session

app = flask.Flask(__name__)


def main():
    configure()
    app.run(debug=True, port=5006)


def configure():
    print("Configuring Flask app:")
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    register_blueprints()
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

    app.register_blueprint(read_views.blueprint)
    app.register_blueprint(update_views.blueprint)
    app.register_blueprint(editor_views.blueprint)
if __name__ == '__main__':
    main()
else:
    configure()
