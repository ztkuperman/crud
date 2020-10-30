import sqlalchemy.orm
from sqlalchemy.orm import session

import crud.data.db_session as db_session
from crud.data.post import Post

test_data = [
    {'id': 1, 'title': "Post 1", "content": "My First Post"},
    {'id': 2, 'title': "Post 2", "content": "My Second Post"},
    {'id': 3, 'title': "Post 3", "content": "My Third Post"},
    ]

## Create
def create_post(title: str, content: str):

    post = Post()
    post.title = title
    post.content = content

    session = db_session.create_session()
    try:
        session.add(post)
        session.commit()
    finally:
        session.close()

    return post.id

## Read
def get_posts():
    session = db_session.create_session()
    try:
        posts = session.query(Post).order_by(Post.id).all()
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
        session.commit()
    finally:
        session.close()
    return

#Delete
def delete_post(id:int):

    session = db_session.create_session()
    try:
        session.query(Post).filter(Post.id==id).delete()
        session.commit()
    finally:
        session.close()

    return


