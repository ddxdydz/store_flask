from flask import Blueprint, request, jsonify

from data.utils.check_api import check_api
from data.utils.upload_image import upload_image

blueprint = Blueprint('send_img', __name__, template_folder='templates')


@blueprint.route('/api/send_img', methods=['POST'])
@check_api
def send_img():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part', "request_files": request.files})
    saved_img_path = upload_image(request.files['file'])
    if not saved_img_path:
        return jsonify({'error': 'Upload img error', "request_files": request.files})
    return jsonify({'path': saved_img_path})
