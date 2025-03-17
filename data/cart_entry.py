import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class CartEntry(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart_entries'
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True, nullable=False)
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'), primary_key=True, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    user = orm.relation('User')
    product = orm.relation('Product')

    def add(self):
        self.count += 1

    def sub(self):
        self.count -= 1
