from flask import request
from flask_restful import abort
from werkzeug.security import check_password_hash

hashed_api_key = "pbkdf2:sha256:150000$rDh6yNZA$ea67d9a507ff96ba276b9c90b4c16eba7087c8f10f2c520815d951202594462b"


def check_api(function):
    def inner(*args, **kwargs):
        from data.utils.Logger import logger
        logger.log_request(request)
        try:
            if not check_password_hash(hashed_api_key, request.headers['apikey']):
                raise Exception
        except Exception:
            abort(403, message='Invalid API-key')
        return function(*args, **kwargs)
    return inner
