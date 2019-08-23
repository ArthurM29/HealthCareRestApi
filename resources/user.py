from flask_restful import Resource, reqparse, abort
from validate_email import validate_email

from models.user import UserModel


# TODO should I move this to a base class ?
def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string.")
    return s


def valid_email(email):
    if not validate_email(email):
        raise ValueError("Invalid email.")
    return email


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('address_1', type=str)
    parser.add_argument('address_2', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('zip_code', type=str)
    parser.add_argument('country', type=str)
    parser.add_argument('phone', type=str)

    @classmethod
    def validate_email(cls, data):
        if not validate_email(data['email']):
            abort(400, message='Invalid email.')

    def post(self):
        """ Create a new user. """
        User.parser.add_argument('confirm_password', type=non_empty_string, required=True,
                                 help='This field cannot be left blank!')
        data = User.parser.parse_args(strict=True)  # return 400 if unexpected arguments received

        User.validate_email(data)

        if UserModel.find_by_email(data['email']):
            abort(400, message="User with email '{}' already exists.".format(data['email']))

        if data['password'] != data['confirm_password']:
            abort(400, message='Passwords do not match.')

        # filter out 'confirm_password' as not present in UserModel
        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}

        user = UserModel(**new_data)
        user.save_to_db()

        return user.to_json(), 201

    def get(self, id=None):
        """ Retrieve all users from DB. """
        if not id:
            return {'users': [user.to_json() for user in UserModel.query.all()]}

        user = UserModel.find_by_id(id)
        if user:
            return user.to_json()
        else:
            abort(404, message='User not found.')

    def put(self, id):
        User.parser.remove_argument('confirm_password')
        data = User.parser.parse_args()
        User.validate_email(data)

        user = UserModel.find_by_id(id)
        if user:
            user.update(data)
            user.save_to_db()
            return user.to_json()

        abort(404, message='User not found.')

    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}

        abort(404, message='User not found.')
