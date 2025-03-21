from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('category_id')
parser.add_argument('name')
parser.add_argument('profile_img_path')
parser.add_argument('short_description')
parser.add_argument('long_description')
parser.add_argument('specifications')
parser.add_argument('promo')
parser.add_argument('price')
parser.add_argument('time')
parser.add_argument('last_edit_time')
