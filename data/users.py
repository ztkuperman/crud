import sqlalchemy as sa
from datetime import datetime as dt

from crud.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True, unique=True)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    password = sa.Column(sa.String, nullable=True, index=True)
    created_date = sa.Column(sa.DateTime, default=dt.now, index=True)
    profile_image = sa.Column(sa.String)
    last_login = sa.Column(sa.DateTime, default=dt.now, index=True)
    #rememberme_token = sa.Column(sa.String, nullable=True)
