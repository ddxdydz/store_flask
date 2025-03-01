from datetime import datetime

from flask import abort, jsonify
from flask_restful import abort, Resource

from api.check_api import check_api
from api.product_resources import abort_if_product_not_found
from api.user_reqparser import *
from api.user_resources import abort_if_user_not_found
from data import db_session
from data.__all_models import *


def abort_if_review_not_found(review_id):
    session = db_session.create_session()
    review = session.query(Review).get(review_id)
    if not review:
        abort(404, message=f"Review {review_id} not found")


class ReviewResource(Resource):
    @check_api
    def get(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        return jsonify({
            'review': review.to_dict(
                only=('id', 'user_id', 'product_id', 'time', 'last_edit_time',
                      'score', 'about', 'profile_img_path'))})

    @check_api
    def delete(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        session.delete(review)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        args = parser.parse_args()
        review = session.query(Review).get(review_id)

        if args['score']:
            review.score = args['score']
        if args['about']:
            review.about = args['about']
        if args['profile_img_path']:
            review.score = args['profile_img_path']
        review.last_edit_time = datetime.now()

        session.commit()
        return jsonify({'success': 'OK'})


class ReviewListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        reviews = session.query(Review).all()
        return jsonify({
            'reviews': [item.to_dict(only=('id', 'user_id', 'product_id', 'score'))
                        for item in reviews]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not all((args['user_id'], args['product_id'])):
            abort(400, message="Bad request to post product")

        review = Review()
        review.user_id = args['user_id']
        review.product_id = args['product_id']
        if args['score']:
            review.score = args['score']
        if args['about']:
            review.about = args['about']
        if args['profile_img_path']:
            review.profile_img_path = args['profile_img_path']

        session.add(review)
        session.commit()
        return jsonify({'success': 'OK'})
