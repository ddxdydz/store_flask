from datetime import datetime


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log_message(self, message):
        with open(f"app.log", "a") as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")

    def log_request(self, rq):
        data = [
            f"API: {int('api' in rq.url)}",
            f"remote_addr: {rq.remote_addr}",
            f"{rq}",
            f"body: {rq.json}",
            f"args: {rq.args}",
            f"form: {rq.form}",
            f"headers: {list(rq.headers.items())}",
        ]
        self.log_message(", ".join(data))


logger = Logger()
logger.log_message("start")


def render_template(*args, **kwargs):
    from flask import request
    from flask import render_template as rt
    logger.log_request(request)
    return rt(*args, **kwargs)


def redirect(*args, **kwargs):
    from flask import request
    from flask import redirect as rd
    logger.log_request(request)
    return rd(*args, **kwargs)


# check_api: logger.log_request(request)
# main: from api.Logger import *
