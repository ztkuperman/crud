import flask
from flask import session
from flask import request, redirect, url_for, flash
from infrastructure.view_modifiers import response
import services.auth_service as auth_svc

blueprint = flask.Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/signup', methods=['get'])
@response(template_file='auth/signup.html')
def signup_get():
    session.pop('_flashes', None)
    return {}


@blueprint.route('/signup', methods=['post'])
@response(template_file='auth/signup.html')
def signup_post():
    form = request.form
    name = form['name']
    email = form['email']
    password = form['password']
    msg = auth_svc.add_new_user(name,email,password)
    if msg == "":
        msg = auth_svc.login_user(form['name'], form['password'])
        return redirect(url_for('read.index'))
    else:
        flash(msg)
        return {}


@blueprint.route('/login', methods=['get'])
@response(template_file='auth/login.html')
def login_get():
    session.pop('_flashes', None)
    return {}


@blueprint.route('/login', methods=['post'])
@response(template_file='auth/login.html')
def login_post():
    form = request.form
    msg = auth_svc.login_user(form['name'], form['password'])
    flash(msg)
    return redirect(url_for('read.index'))


@blueprint.route('/logout')
@response(template_file='auth/logout.html')
def logout():
    auth_svc.logout_user()
    return {}







