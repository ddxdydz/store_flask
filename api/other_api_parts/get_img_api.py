import os

from flask import Blueprint, request, jsonify, send_file, abort

from api.check_api import check_api
from data.upload_tools.project_root import PROJECT_ROOT

blueprint = Blueprint('get_img', __name__, template_folder='templates')


@blueprint.route('/api/get_img')
@check_api
def get_img():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['path']):
        return jsonify({'error': 'Bad request'})
    path = os.path.join(PROJECT_ROOT, request.json['path'])
    if not os.path.exists(path):
        return jsonify({'error': 'Path does not exist'})
    try:
        return send_file(path)
    except FileNotFoundError:
        abort(404)
