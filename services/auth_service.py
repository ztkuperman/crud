from flask import session
import crud.data.db_session as db_session
from crud.data.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError


# Sign up
def add_new_user(name,email,password):
    user = User()
    user.name = name
    user.email = email
    user.password = generate_password_hash(password)

    sess = db_session.create_session()
    try:
        sess.add(user)
        sess.commit()
    except IntegrityError as e:
        if e.orig.args[0].find("UNIQUE") == 0:
            return "Username already exists."
    finally:
        sess.close()
    return ""

# Login
def login_user(name, password):

    sess = db_session.create_session()
    try:
        user = sess.query(User).filter(User.name == name).first()
        if check_password_hash(user.password, password):
            user.last_login = dt.now()
            sess.commit()
            session['username'] = user.name
            return True
        else:
            return False
    finally:
        sess.close()


# Logout
def logout_user():
    session.pop('username')
