from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class OrderEntry(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_entries'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True,
        primary_key=True, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, default="Нет данных")
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    role = orm.relation('User')

    def update_time(self):
        self.time = datetime.now()
