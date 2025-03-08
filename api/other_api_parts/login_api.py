from flask import Blueprint, request, jsonify

import data.db_session as db_session
from data.user import User

blueprint = Blueprint('login_api', __name__, template_folder='templates')


@blueprint.route('/api/check_authorization_data')
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['email', 'password']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = session.query(User).filter(User.email == request.json['email']).first()
    if user and user.check_password(request.json['password']):
        return jsonify({'result': True})
    return jsonify({'result': False})
