from flask import abort, jsonify
from flask_restful import abort, Resource

from api.card_entry_reqparser import *
from api.check_api import check_api
from data import db_session
from data.__all_models import *


def abort_if_card_entry_not_found(user_id, product_id):
    session = db_session.create_session()
    card_entry = session.query(CardEntry).filter(
        CardEntry.user_id == user_id, CardEntry.product_id == product_id).first()
    if not card_entry:
        abort(404, message=f"Card_entry {(user_id, product_id)} not found")


class CardEntryResource(Resource):
    @check_api
    def get(self, user_id, product_id):
        abort_if_card_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        card_entry = session.query(CardEntry).get((user_id, product_id))
        return jsonify({
            'card_entry': card_entry.to_dict(
                only=('user_id', 'product_id', 'count'))})

    @check_api
    def delete(self, user_id, product_id):
        abort_if_card_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        card_entry = session.query(CardEntry).get((user_id, product_id))
        session.delete(card_entry)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, user_id, product_id):
        abort_if_card_entry_not_found(user_id, product_id)
        session = db_session.create_session()
        args = parser.parse_args()
        card_entry = session.query(CardEntry).get((user_id, product_id))

        if args['count']:
            card_entry.count = args['count']

        session.commit()
        return jsonify({'success': 'OK'})


class CardEntryListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        card_entries = session.query(CardEntry).all()
        return jsonify({
            'card_entries': [item.to_dict(only=('user_id', 'product_id', 'count'))
                             for item in card_entries]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not all((args['user_id'], args['product_id'])):
            abort(400, message="Bad request to post card entry")

        card_entry = CardEntry()
        card_entry.product_id = args['product_id']
        card_entry.user_id = args['user_id']

        session.add(card_entry)
        session.commit()
        return jsonify({'success': 'OK'})
