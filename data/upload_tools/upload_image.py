import os
from time import time

from data.upload_tools.project_root import PROJECT_ROOT

UPLOAD_IMAGES_FOLDER = os.path.join('static', 'imgs', 'uploaded')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def upload_image(img_data) -> str:
    if not img_data:
        return ''
    if '.' not in img_data.filename:
        return ''
    extension = img_data.filename.split('.')[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return ''
    img_name = f"{str(round(time() * 1000))}.{extension}"
    img_path = os.path.join(UPLOAD_IMAGES_FOLDER, img_name)
    img_data.save(os.path.join(PROJECT_ROOT, UPLOAD_IMAGES_FOLDER, img_name))
    return img_path.replace('\\', '/')
