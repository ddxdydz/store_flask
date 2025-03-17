from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True,
        primary_key=True, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    category_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, default="Без названия")
    profile_img_path = sqlalchemy.Column(sqlalchemy.String, default='static/imgs/noimg.jpg')
    short_description = sqlalchemy.Column(sqlalchemy.String, default="Нет данных")
    long_description = sqlalchemy.Column(sqlalchemy.String, default="Нет данных")
    specifications = sqlalchemy.Column(sqlalchemy.String, default="Нет данных")
    promo = sqlalchemy.Column(sqlalchemy.String, default="Нет")
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    last_edit_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    user = orm.relation('User')
    category = orm.relation('Category')
