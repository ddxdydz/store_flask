from flask_restful import reqparse

parser = reqparse.RequestParser()
# user_id, product_id - primary key
parser.add_argument('user_id')
parser.add_argument('product_id')
parser.add_argument('count')
