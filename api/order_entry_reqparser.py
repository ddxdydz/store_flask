from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('description')
parser.add_argument('time')
