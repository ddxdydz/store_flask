import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=False)
