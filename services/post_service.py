import sqlalchemy.orm
from sqlalchemy.orm import session

import crud.data.db_session as db_session
from crud.data.post import Post
from datetime import datetime as dt

## Create
def create_post(title: str, content: str, author:str):

    post = Post()
    post.title = title
    post.content = content
    post.author = author
    post.pub_status = 'private'

    session = db_session.create_session()
    try:
        session.add(post)
        session.commit()
    finally:
        session.close()

    return post.id

## Read
def get_posts(author='%', status='%'):
    filters = {'author':author,'pub_status':status}
    session = db_session.create_session()
    try:
        query = session.query(Post)
        for column, value in filters.items():
            query = query.filter(getattr(Post,column).like(value))
        posts = query.order_by(Post.modified_date.desc()).all()
    finally:
        session.close()
    return posts


def get_single_post(id: int):
    session = db_session.create_session()
    try:
        post = session.query(Post).filter(Post.id == id).first()
    finally:
        session.close()
    return post

## Update
def update_post(id:int, title: str, content: str):

    session = db_session.create_session()
    try:
        post = session.query(Post).filter(Post.id == id).first()
        post.title = title
        post.content = content
        post.modified_date = dt.now()
        session.commit()
    finally:
        session.close()
    return


def update_publish(id:int, status:str):
    session = db_session.create_session()
    try:
        post = session.query(Post).filter(Post.id==id).first()
        old_status = post.pub_status
        post.pub_status = status
        session.commit()
    finally:
        session.close()
    return (old_status, status)


## Delete
def delete_post(id:int):

    session = db_session.create_session()
    try:
        session.query(Post).filter(Post.id==id).delete()
        session.commit()
    finally:
        session.close()

def remove_user_posts(name):
    sess = db_session.create_session()
    try:
        posts = sess.query(Post).filter(Post.author==name).all()
        for p in posts:
            p.author = "<deleted>"
            p.pub_status = "draft"
        sess.commit()
    finally:
        sess.close()
