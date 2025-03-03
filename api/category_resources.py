from flask import abort, jsonify
from flask_restful import abort, Resource

from api.category_reqparser import *
from api.check_api import check_api
from data import db_session
from data.__all_models import *


def abort_if_category_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Category {category_id} not found")


class CategoryResource(Resource):
    @check_api
    def get(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        return jsonify({
            'category': category.to_dict(
                only=('id', 'name'))})

    @check_api
    def delete(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        args = parser.parse_args()
        category = session.query(Category).get(category_id)

        if args['name']:
            category.name = args['name']

        session.commit()
        return jsonify({'success': 'OK'})


class CategoryListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({
            'categories': [item.to_dict(only=('id', 'name'))
                           for item in categories]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not args['name']:
            abort(400, message="Bad request to post category")

        category = Category()
        category.name = args['name']

        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})
