from flask_restful import Resource, reqparse
from validate_email import validate_email

from models.user import UserModel


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string.")
    return s


def valid_email(email):
    if not validate_email(email):
        raise ValueError("Invalid email.")
    return email


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('confirm_password', type=non_empty_string, required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('user_name', type=str)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('address_1', type=str)
    parser.add_argument('address_2', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('zip_code', type=str)
    parser.add_argument('country', type=str)
    parser.add_argument('phone', type=str)

    def post(self):
        """ Create a new user. """
        data = UserRegister.parser.parse_args()

        if not validate_email(data['email']):
            return {'message': 'Invalid email.'}, 400

        if UserModel.find_by_email(data['email']):
            return {'message': "User with email '{}' already exists.".format(data['email'])}, 400

        if data['password'] != data['confirm_password']:
            return {'message': 'Passwords do not match.'}, 400

        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}  # 'confirm_password' not present in UserModel

        user = UserModel(**new_data)
        user.save_to_db()
        return user.to_json(), 201
