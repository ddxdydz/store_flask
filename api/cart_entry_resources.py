from flask import abort, jsonify
from flask_restful import abort, Resource

from api.cart_entry_reqparser import *
from data import db_session
from data.__all_models import *
from data.utils.check_api import check_api


def abort_if_cart_entry_not_found(user_id, product_id):
    session = db_session.create_session()
    cart_entry = session.query(CartEntry).filter(
        CartEntry.user_id == user_id, CartEntry.product_id == product_id).first()
    if not cart_entry:
        abort(404, message=f"cart_entry {(user_id, product_id)} not found")


class CartEntryResource(Resource):
    @check_api
    def get(self, user_id, product_id):
        abort_if_cart_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        cart_entry = session.query(CartEntry).get((user_id, product_id))
        return jsonify({
            'cart_entry': cart_entry.to_dict(
                only=('user_id', 'product_id', 'count'))})

    @check_api
    def delete(self, user_id, product_id):
        abort_if_cart_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        cart_entry = session.query(CartEntry).get((user_id, product_id))
        session.delete(cart_entry)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, user_id, product_id):
        abort_if_cart_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        args = parser.parse_args()
        cart_entry = session.query(CartEntry).get((user_id, product_id))

        cart_entry.count = int(args['count'])

        session.commit()
        return jsonify({'success': 'OK'})


class CartEntryListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        cart_entries = session.query(CartEntry).all()
        return jsonify({
            'cart_entries': [item.to_dict(only=('user_id', 'product_id', 'count'))
                             for item in cart_entries]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not all((args['user_id'], args['product_id'])):
            abort(400, message="Bad request to post cart entry")

        cart_entry = CartEntry()
        cart_entry.product_id = args['product_id']
        cart_entry.user_id = args['user_id']

        session.add(cart_entry)
        session.commit()
        return jsonify({'success': 'OK', 'user_id': cart_entry.user_id, 'product_id': cart_entry.product_id})
