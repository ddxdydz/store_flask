from flask import request
from flask_restful import abort
from werkzeug.security import check_password_hash

from main import hashed_api_key


def check_api(function):
    def inner(*args, **kwargs):
        try:
            if not check_password_hash(hashed_api_key, request.headers['apikey']):
                raise Exception
        except Exception:
            abort(403, message='Invalid API-key')
        return function(*args, **kwargs)
    return inner
