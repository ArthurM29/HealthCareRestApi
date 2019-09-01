from flask_restful import reqparse, fields, marshal_with, abort

from models.user import UserModel, UserSchema
from resources.base_resource import BaseResource
from common.types import email, non_empty_string


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
        data = cls.parser.parse_args(strict=True)
        if UserModel.find_by_email(data['email']):
            abort(400, message="User with email '{}' already exists.".format(data['email']))

        if data['password'] != data['confirm_password']:
            abort(400, message='Passwords do not match.')

        # filter out 'confirm_password' as not present in UserModel
        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return new_data
