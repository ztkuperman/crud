import flask
from flask import request, redirect, url_for, flash, session, after_this_request
from infrastructure.view_modifiers import response
import services.user_service as user_svc
import datetime

blueprint = flask.Blueprint('user', __name__, template_folder='templates')

## Signup
@blueprint.route('/signup', methods=['get'])
@response(template_file='user/signup.html')
def signup_get():
    session.pop('_flashes', None)
    return {"csrf_token":user_svc.csrf_new_token()}


@blueprint.route('/signup', methods=['post'])
@response(template_file='user/signup.html')
def signup_post():
    form = request.form
    name = form['name']
    email = form['email']
    password = form['password']
    csrf_token = form['csrf_token']

    csrf_valid = user_svc.csrf_validate(csrf_token)
    msg = user_svc.add_new_user(name,email,password)
    if msg == "" and csrf_valid:
        msg = user_svc.login_user(form['name'], form['password'])
        return redirect(url_for('read.index'))
    else:
        flash(msg)
        return {"csrf_token":user_svc.csrf_new_token()}

## Login & Logout
@blueprint.route('/login', methods=['get'])
@response(template_file='user/login.html')
def login_get():
    session.pop('_flashes', None)
    return {'csrf_token':user_svc.csrf_new_token()}


@blueprint.route('/login', methods=['post'])
@response(template_file='user/login.html')
def login_post():
    form = request.form
    name = form.get('name')
    password = form.get('password')
    csrf_valid = user_svc.csrf_validate(form['csrf_token'])
    if user_svc.login_user(name, password) and csrf_valid:
        if form.get('rememberme'):
            rememberme_token = user_svc.rememberme_new_token(name)
            @after_this_request
            def set_cookies(response):
                cookie_life = datetime.timedelta(7)
                exp_date = datetime.datetime.now() + cookie_life
                response.set_cookie('username', name, expires=exp_date)
                response.set_cookie('rememberme', rememberme_token, expires=exp_date)
                return response
    else:
        flash("Invalid Credentials.")
        return {'csrf_token': user_svc.csrf_new_token()}
    return redirect(url_for('read.index'))


@blueprint.route('/logout')
@response(template_file='user/logout.html')
def logout():
    user_svc.logout_user()
    @after_this_request
    def set_cookies(response):
        response.set_cookie('username', '', expires=0)
        response.set_cookie('rememberme', '', expires=0)
        return response
    return {}

## Auth check
@blueprint.before_app_request
def authentication_check():
    # Check if any users exist
    if not user_svc.users_exist():
        redirect(url_for('auth.admin_signup_get'))
    # Check if the user needs to be logged in via RememberMe
    if session.get('username') == None:
        name = request.cookies.get('username')
        token = request.cookies.get('rememberme')
        if name and token:
            user_svc.rememberme_validate(name,token)
        else:
            session['username'] = "Reader"
            session['role'] = "Guest"
    # Make sure a CSRF token list exists
    if session.get('csrf_tokens') == None:
        session['csrf_tokens'] = []
