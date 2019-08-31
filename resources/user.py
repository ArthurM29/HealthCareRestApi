from flask_restful import reqparse, abort, fields, marshal_with

from models.user import UserModel
from resources.base_resource import BaseResource
from common.types import email, non_empty_string


# exclude password from response
user_response_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "address_1": fields.String,
    "address_2": fields.String,
    "city": fields.String,
    "state": fields.String,
    "zip_code": fields.String,
    "country": fields.String,
    "phone": fields.String,
    "user_level": fields.String
}


class User(BaseResource):
    name = 'user'
    model = UserModel

    parser = reqparse.RequestParser()
    parser.add_argument('email', location='json', type=email, required=True)
    parser.add_argument('password', location='json', type=non_empty_string, required=True)
    parser.add_argument('confirm_password', location='json', type=non_empty_string, required=True)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('address_1', type=str)
    parser.add_argument('address_2', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('zip_code', type=str)
    parser.add_argument('country', type=str)
    parser.add_argument('phone', type=str)
    parser.add_argument('user_level', type=str)

    @classmethod
    def validate_arguments(cls):
        data = User.parser.parse_args(strict=True)  # return 400 if unexpected arguments received

        if UserModel.find_by_email(data['email']):
            abort(400, message="User with email '{}' already exists.".format(data['email']))

        if data['password'] != data['confirm_password']:
            abort(400, message='Passwords do not match.')

        # filter out 'confirm_password' as not present in UserModel
        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return new_data

    @marshal_with(user_response_fields)
    def get(self, id=None):
        return super().get(id=id)

    def post(self):
        # TODO should post return Location header with full URI of the created resource ?
        """ Create a new user. """
        data = User.validate_arguments()
        user = UserModel(**data)
        user.save_to_db()

        return user.json(), 201

    def put(self, id):
        """ Update user by id. """

        # if UserModel.find_by_email(data['email']) and data['email'] != user.email:
        #     abort(400, message="User with email '{}' already exists.".format(data['email']))

        user = UserModel.find_by_id(id)

        if user:
            data = User.validate_arguments()
            user.update(data)
            user.save_to_db()
            return user.json()

        abort(404, message='User not found.')
