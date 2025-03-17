from flask import abort, jsonify
from flask_restful import abort, Resource

from api.order_entry_reqparser import *
from data import db_session
from data.__all_models import *
from data.utils.check_api import check_api


def abort_if_order_not_found(order_id):
    session = db_session.create_session()
    order = session.query(OrderEntry).get(order_id)
    if not order:
        abort(404, message=f"Order {order_id} not found")


class OrderEntryResource(Resource):
    @check_api
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(OrderEntry).get(order_id)
        return jsonify({
            'order': order.to_dict(
                only=('id', 'user_id', 'description', 'time'))})

    @check_api
    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(OrderEntry).get(order_id)
        session.delete(order)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        args = parser.parse_args()
        order = session.query(OrderEntry).get(order_id)

        if args['user_id']:
            order.user_id = args['user_id']
        if args['description']:
            order.description = args['description']
        if args['time']:
            order.time = args['time']

        session.commit()
        return jsonify({'success': 'OK'})


class OrderEntryListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        orders = session.query(OrderEntry).all()
        return jsonify({
            'orders': [item.to_dict(only=('id', 'description', 'user_id'))
                       for item in orders]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not args['user_id']:
            abort(400, message="Bad request to post OrderEntry")

        order = OrderEntry()
        order.user_id = args['user_id']
        if args['description']:
            order.description = args['description']
        if args['time']:
            order.time = args['time']

        session.add(order)
        session.commit()
        return jsonify({'success': 'OK', 'order_id': order.id})
