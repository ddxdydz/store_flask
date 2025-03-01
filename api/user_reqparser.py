from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('role_id')
parser.add_argument('balance')
parser.add_argument('about')
parser.add_argument('profile_img_path')
