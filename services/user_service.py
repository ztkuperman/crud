from flask import session
import crud.data.db_session as db_session
from crud.data.users import User
import services.post_service as post_svc
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError
import os
import base64

#### User authentication
## Sign up
def add_new_user(name,email,password, role='reader'):
    user = User()
    user.name = name
    user.email = email
    user.password = generate_password_hash(password)
    user.role = role
    user.status = 'active'

    sess = db_session.create_session()
    try:
        sess.add(user)
        sess.commit()
    except IntegrityError as e:
        if e.orig.args[0].find("UNIQUE") == 0:
            return "Username already exists."
    finally:
        sess.close()


## Login
def login_user(name, password='', remembered=False):

    sess = db_session.create_session()
    try:
        user = sess.query(User).filter(User.name == name).first()
        if (check_password_hash(user.password, password) or remembered) \
            and user.status == "active":
            user.last_login = dt.now()
            sess.commit()
            session['username'] = user.name
            session['role'] = user.role
            session['logged_in'] = True
            print(f'User {user.name} sucessfully logged in.')
            return True
    except:
        pass
    finally:
        sess.close()
    return False


## Logout
def logout_user():
    name = session['username']
    sess = db_session.create_session()
    print(f'User {name} logged out.')
    try:
        user = sess.query(User).filter(User.name == name).first()
        user.rememberme_token = None
        sess.commit()
    finally:
        sess.close()
    session.clear()
    session['username'] = "Reader"
    session['role'] = "Guest"



#### Remember Me tokens
# Design Decisions:
# If a new session starts and the username and rememberme cookies are
# present and valid, then the user can be automatically logged in.
# This means a rememberme cookie acts like a password for auth purposes.
# Therefore, the rememberme cookie must be secured like a password.
# Like a password, the token is hashed before being stored in the DB.

def rememberme_new_token(name):
    sess = db_session.create_session()
    try:
        user = sess.query(User).filter(User.name == name).first()
        rememberme_token = base64.b64encode(os.urandom(32)).decode('ascii')
        user.rememberme_token = generate_password_hash(rememberme_token)
        sess.commit()
    finally:
        sess.close()
    return rememberme_token


def rememberme_validate(name, token):
    sess = db_session.create_session()
    try:
        user = sess.query(User).filter(User.name == name).first()
        expired = (dt.now() - user.last_login).days > 7
        valid = check_password_hash(user.rememberme_token,token)
        if valid and not expired:
            login_user(name, remembered=True)
    finally:
        sess.close()

#### CSRF Tokens
# Design Decisions:
# These functions can be used to create new random tokens for each form.
# The view method can have the token validated to prevent CSRF attacks.
# Each new token is added to a token list stored in the session.
# Once validated, the token is removed from the list.
# If the session ends (i.e. the browser is closed), all CSRF tokens are
# invalidated.
def csrf_new_token():
    csrf_token = base64.b64encode(os.urandom(32)).decode('ascii')
    session['csrf_tokens'].append(csrf_token)
    return csrf_token

def csrf_validate(token):
    if token in session['csrf_tokens']:
        session['csrf_tokens'].remove(token)
        return True
    else:
        return False

# User Update/Delete functions

def user_authorization_get():
    sess = db_session.create_session()
    try:
        users = sess.query(User).all()
        auth_data = {user.name:[user.role,user.status] for user in users}
    finally:
        sess.close()
    return auth_data


def user_authorization_update(new_user_auth):
    old_user_auth = user_authorization_get()
    sess = db_session.create_session()

    try:
        count=0
        users = sess.query(User).all() # Remove this line
        for name,[role,status] in new_user_auth.items():
            if old_user_auth[name] != new_user_auth[name]:
                if status == 'deleted':
                    post_svc.remove_user_posts(name)
                    sess.query(User).filter(User.name==name).delete()
                else: # For every other status change
                    user = sess.query(User).filter(User.name == name).first()
                    user.role = role
                    user.status = status
                count += 1
        sess.commit()
    finally:
        sess.close()
    return f'Updated {count} records.'


#Helper/Utility functions
def get_user_by_name(name:str):
    sess = db_session.create_session()
    try:
        user = sess.query(User).filter(User.name == name).first()
    finally:
        sess.close()
    return user

def users_exist():
    sess = db_session.create_session()
    try:
        if sess.query(User).count() > 0:
            return True
        else:
            return False
    finally:
        sess.close()
