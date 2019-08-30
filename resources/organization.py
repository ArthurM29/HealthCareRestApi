from flask_restful import Resource, reqparse, abort
from validate_email import validate_email

from models.user import UserModel
from models.organization import OrganizationModel
from resources.base_resource import BaseResource


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string.")
    return s


class Organization(BaseResource):
    name = 'organization'
    model = OrganizationModel

    parser = reqparse.RequestParser()
    parser.add_argument('admin_email', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=non_empty_string, required=True, help='This field cannot be left blank!')
    parser.add_argument('confirm_password', type=non_empty_string, required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('admin_first_name', type=str)
    parser.add_argument('admin_last_name', type=str)
    parser.add_argument('organization_name', type=str)
    parser.add_argument('organization_address_1', type=str)
    parser.add_argument('organization_address_2', type=str)
    parser.add_argument('organization_city', type=str)
    parser.add_argument('organization_state', type=str)
    parser.add_argument('organization_zip_code', type=str)
    parser.add_argument('organization_country', type=str)
    parser.add_argument('organization_phone', type=str)

    @classmethod
    def validate_email(cls, data):
        if not validate_email(data['admin_email']):
            abort(400, message='Invalid email.')
        data['admin_email'] = data['admin_email'].lower()

    @classmethod
    def validate_arguments(cls):
        data = Organization.parser.parse_args(strict=True)  # return 400 if unexpected arguments received
        Organization.validate_email(data)

        if UserModel.find_by_email(data['admin_email']):
            abort(400, message="User with email '{}' already exists.".format(data['admin_email']))

        if data['password'] != data['confirm_password']:
            abort(400, message='Passwords do not match.')

        # filter out 'confirm_password' as not present in UserModel
        new_data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return new_data

    def post(self):
        # TODO should post return Location header with full URI of the created resource ?
        """ Create a new organization. """
        data = Organization.validate_arguments()
        user = UserModel(email=data['admin_email'], password=data['password'], first_name=data['admin_first_name'],
                         last_name=data['admin_last_name'], user_level='admin')

        user.save_to_db()

        org = OrganizationModel(name=data['organization_name'],
                                address_1=data['organization_address_1'],
                                address_2=data['organization_address_2'],
                                city=data['organization_city'],
                                state=data['organization_state'],
                                zip_code=data['organization_zip_code'],
                                country=data['organization_country'],
                                phone=data['organization_phone'],
                                admin_id=user.id)
        org.save_to_db()

        return {"admin": user.json(), "organization": org.json()}, 201

    def delete(self, id):
        abort(405)


#TODO do we need put and delete for this ?