import os
from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True,
        primary_key=True, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    last_edit_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    about = sqlalchemy.Column(sqlalchemy.String, default="Не указано")
    profile_img_path = sqlalchemy.Column(sqlalchemy.String, default='')

    user = orm.relation('User')
    category = orm.relation('Product')
