import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    count_wins = sqlalchemy.Column(sqlalchemy.Integer)
    count_loses = sqlalchemy.Column(sqlalchemy.Integer)
    money = sqlalchemy.Column(sqlalchemy.Integer)
