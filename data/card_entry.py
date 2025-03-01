import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class CardEntry(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'card_entries'
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True, nullable=False)
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'), primary_key=True, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    user = orm.relation('User')
    category = orm.relation('Product')

    def increase(self):
        self.count += 1

    def decrease(self):
        self.count -= 1
