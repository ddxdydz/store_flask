from flask import abort, jsonify
from flask_restful import abort, Resource

from api.check_api import check_api
from api.user_reqparser import *
from data import db_session
from data.__all_models import *
from forms.validators.EmailValidator import is_email_valid


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    @check_api
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({
            'user': users.to_dict(
                only=('id', 'name', 'email', 'hashed_password', 'role_id', 'balance', 'about',
                      'profile_img_path', 'time'))})

    @check_api
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)

        user.set_password("deleted3424jl23")

        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        args = parser.parse_args()
        user = session.query(User).get(user_id)

        if args['password']:
            user.set_password(args['password'])
        if args['role_id']:
            user.title = args['role_id']
        if args['balance']:
            user.title = args['balance']
        if args['about']:
            user.title = args['about']
        if args['profile_img_path']:
            user.title = args['profile_img_path']

        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(only=('id', 'name', 'email', 'role_id')) 
                      for item in users]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if not all((args['name'], args['email'], args['password'])):
            abort(400, message="Bad request to post user")

        if not is_email_valid(args['email']):
            return jsonify({'success': 'NO', 'correct_email': False})
        if session.query(User).filter(User.email == args['email']).first():
            return jsonify({'success': 'NO', 'correct_email': True, 'unique_email': False})

        user = User()
        user.name = args['name']
        user.set_password(args['password'])
        user.email = args['email']
        if args['role_id']:
            user.role_id = args['role_id']
        if args['balance']:
            user.balance = args['balance']
        if args['about']:
            user.about = args['about']
        if args['profile_img_path']:
            user.profile_img_path = args['profile_img_path']

        session.add(user)
        session.commit()
        user_id = session.query(User).filter(User.email == args['email']).first().id
        return jsonify({'success': 'OK', 'correct_email': True, 'unique_email': True, 'user_id': user_id})
