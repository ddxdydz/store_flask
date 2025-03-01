from datetime import datetime

from flask import abort, jsonify
from flask_restful import abort, Resource

from api.category_resources import abort_if_category_not_found
from api.check_api import check_api
from api.user_reqparser import *
from api.user_resources import abort_if_user_not_found
from data import db_session
from data.__all_models import *


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


class ProductResource(Resource):
    @check_api
    def get(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify({
            'product': product.to_dict(
                only=('id', 'user_id', 'category_id', 'name', 'profile_img_path', 'short_description',
                      'long_description', 'specifications', 'promo', 'price', 'price_title',
                      'time', 'last_edit_time'))})

    @check_api
    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        args = parser.parse_args()
        product = session.query(Product).get(product_id)

        if args['category_id']:
            product.category_id = args['category_id']
        if args['name']:
            product.name = args['name']
        if args['profile_img_path']:
            product.profile_img_path = args['profile_img_path']
        if args['short_description']:
            product.short_description = args['short_description']
        if args['long_description']:
            product.long_description = args['long_description']
        if args['specifications']:
            product.specifications = args['specifications']
        if args['promo']:
            product.promo = args['promo']
        if args['price']:
            product.price = args['price']
        if args['price_title']:
            product.price_title = args['price_title']
        product.last_edit_time = datetime.now()

        session.commit()
        return jsonify({'success': 'OK'})


class ProductListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({
            'products': [item.to_dict(only=('id', 'user_id', 'category_id', 'name', 'price'))
                         for item in products]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not all((args['user_id'], args['category_id'])):
            abort(400, message="Bad request to post product")

        product = Product()
        product.user_id = args['user_id']
        product.category_id = args['category_id']
        if args['name']:
            product.name = args['name']
        if args['profile_img_path']:
            product.profile_img_path = args['profile_img_path']
        if args['short_description']:
            product.short_description = args['short_description']
        if args['long_description']:
            product.long_description = args['long_description']
        if args['specifications']:
            product.specifications = args['specifications']
        if args['promo']:
            product.promo = args['promo']
        if args['price']:
            product.price = args['price']
        if args['price_title']:
            product.price_title = args['price_title']

        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})
