from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('product_id')
parser.add_argument('time')
parser.add_argument('last_edit_time')
parser.add_argument('score')
parser.add_argument('about')
parser.add_argument('profile_img_path')
