import flask
from flask import request, redirect, url_for, flash, session, after_this_request
from infrastructure.view_modifiers import response
import services.auth_service as auth_svc
import datetime

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
    name = form['name']
    valid =  auth_svc.login_user(name, form['password'])
    if valid:
        if form['rememberme']:
            rememberme_token = auth_svc.set_rememberme(name)
            @after_this_request
            def set_cookies(response):
                cookie_life = datetime.timedelta(7)
                exp_date = datetime.datetime.now() + cookie_life
                response.set_cookie('username', name, expires=exp_date)
                response.set_cookie('rememberme', rememberme_token, expires=exp_date)
                return response
    else:
        flash("Invalid Credentials.")
        return {}
    return redirect(url_for('read.index'))


@blueprint.route('/logout')
@response(template_file='auth/logout.html')
def logout():
    auth_svc.logout_user()
    @after_this_request
    def set_cookies(response):
        response.set_cookie('username', '', expires=0)
        response.set_cookie('rememberme', '', expires=0)
        return response
    return {}
