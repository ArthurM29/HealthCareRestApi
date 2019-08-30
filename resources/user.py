from flask_restful import reqparse, abort
from validate_email import validate_email

from models.user import UserModel
from resources.base_resource import BaseResource


# TODO should I move this to a base class ?
def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string.")
    return s


class User(BaseResource):
    name = 'user'
    model = UserModel

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('confirm_password', type=non_empty_string, required=True,
                             help='This field cannot be left blank!')
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
    def validate_email(cls, data):
        if not validate_email(data['email']):
            abort(400, message='Invalid email.')
        data['email'] = data['email'].lower()

    @classmethod
    def validate_arguments(cls):
        data = User.parser.parse_args(strict=True)  # return 400 if unexpected arguments received
        User.validate_email(data)

        if UserModel.find_by_email(data['email']):
            abort(400, message="User with email '{}' already exists.".format(data['email']))

        if data['password'] != data['confirm_password']:
            abort(400, message='Passwords do not match.')

        # filter out 'confirm_password' as not present in UserModel
        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return new_data

    def post(self):
        #TODO should post return Location header with full URI of the created resource ?
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


