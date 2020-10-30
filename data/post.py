import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
from crud.data.modelbase import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True, index=True)
    title: str = sa.Column(sa.String, nullable=False)
    content: str = sa.Column(sa.Text, nullable=False)

#    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
#    last_updated: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
 #   author: str = sa.Column(sa.String)

    def __repr__(self):
        return '<Post {}>'.format(self.id)
