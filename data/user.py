import os
from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True,
        primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String, nullable=False)
    role_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'), default=2)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    about = sqlalchemy.Column(sqlalchemy.String, default="Это описание профиля пользователя. Здесь можно указать интересы и другую информацию.")
    profile_img_path = sqlalchemy.Column(sqlalchemy.String, default=os.path.join('static', 'imgs', 'noimg.jpg'))
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    role = orm.relation('Role')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def add_to_balance(self, num: int):
        self.balance += num

    def sub_to_balance(self, num: int):
        self.balance -= num

    def check_balance(self, num: int):
        return self.balance >= num

    def __repr__(self):
        return f'<User> {self.name} {self.role}'
