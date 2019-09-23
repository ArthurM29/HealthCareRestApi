import json

from common.utils import random_string, run_db_query
from test_framework.api.users_api import UsersAPI
from termcolor import colored
import pytest
from pytest import mark as m

from assertpy import assert_that

max_length_exceed_cases = [("empty_email", ""),
                           ("email_without_local_part", "@mac.com"),
                           ("email_without_@", "myemailmac.com"),
                           ("email_without_dot", "myemail@maccom"),
                           ("email_without_domain", "myemail@mac.")]


@pytest.fixture
def users_api():
    return UsersAPI(debug=True)


@m.describe("Create User")
class TestCreateUser:

    @m.it("Verify required field error is returned if email is skipped")
    def test_email_is_required_if_skipped(self, users_api):
        users_api.payload.remove_field('email')
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['email'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if email == empty string")
    def test_email_is_required_if_empty_string(self, users_api):
        users_api.payload.email = ''
        response = users_api.create_user()
        assert response.status_code == 400
        assert_that(response.json()['message']['email']).contains('Not a valid email address.')
        assert_that(response.json()['message']['email']).contains('Length must be between 1 and 250.')

    @m.it("Verify only valid email values are accepted")
    @pytest.mark.parametrize("case, email", max_length_exceed_cases)
    def test_email_format_is_validated(self, case, email, users_api):
        print(colored("\n\nRunning test_framework case: {}".format(case), color='yellow'))
        users_api.payload.email = email
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['email'][0] == 'Not a valid email address.'
        print("\nTest case: {} {}".format(case, colored('PASSED', 'green')))

    @m.it("Verify email is unique")
    def test_email_is_unique(self, users_api):
        response1 = users_api.create_user()
        assert response1.status_code == 201
        response2 = users_api.create_user()
        assert response2.status_code == 400
        assert response2.json()['message'] == "user.email already exists"

    @m.it("Verify email is lowercased before storing in the DB")
    def test_email_is_lowercased(self, users_api):
        email = "MYEMAIL+" + random_string(6) + "@gmail.com"
        users_api.payload.email = email
        response = users_api.create_user()
        assert response.status_code == 201
        assert response.json()['email'] == email.lower()

    @m.it("Verify required field error is returned if password is skipped")
    def test_password_is_required_skipped(self, users_api):
        users_api.payload.remove_field('password')
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['password'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if password == empty string")
    def test_password_is_required_if_empty_string(self, users_api):
        users_api.payload.password = ''
        response = users_api.create_user()
        assert response.status_code == 400
        assert_that(response.json()['message']['password']).contains('Length must be between 1 and 128.')

    @m.it("Verify required field error is returned if confirm_password is skipped")
    def test_confirm_password_is_required_if_skipped(self, users_api):
        users_api.payload.remove_field('confirm_password')
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['confirm_password'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if confirm_password == empty string")
    def test_confirm_password_is_required_if_empty_string(self, users_api):
        users_api.payload.confirm_password = ''
        response = users_api.create_user()
        assert response.status_code == 400
        assert_that(response.json()['message']['confirm_password']).contains('Length must be between 1 and 128.')

    @m.it("Verify required field error is returned if user_level is skipped")
    def test_user_level_is_required_if_skipped(self, users_api):
        users_api.payload.remove_field('user_level')
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['user_level'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if user_level == empty string")
    def test_user_level_is_required_if_empty_string(self, users_api):
        users_api.payload.user_level = ''
        response = users_api.create_user()
        assert response.status_code == 400
        assert_that(response.json()['message']['user_level']).contains('Must be one of: admin, user.')

    @m.it("Verify user_level field accepts value 'admin'")
    def test_user_level_accepts_admin_value(self, users_api):
        users_api.payload.user_level = 'admin'
        response = users_api.create_user()
        assert response.status_code == 201
        assert response.json()['user_level'] == 'admin'

    @m.it("Verify user_level field accepts value 'user'")
    def test_user_level_accepts_user_value(self, users_api):
        users_api.payload.user_level = 'user'
        response = users_api.create_user()
        assert response.status_code == 201
        assert response.json()['user_level'] == 'user'

    @m.it("Verify user_level field rejects values different from ['admin', 'user']")
    def test_user_level_rejects_random_values(self, users_api):
        users_api.payload.user_level = 'someone'
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message']['user_level'][0] == 'Must be one of: admin, user.'

    @m.it("Verify user_level is lowercased before storing in the DB")
    def test_user_level_is_lowercased(self, users_api):
        users_api.payload.user_level = 'ADMIN'
        response = users_api.create_user()
        assert response.status_code == 201
        assert response.json()['user_level'] == 'admin'

    @m.it("Verify able to create a user without providing optional fields")
    def test_optional_fields(self, users_api):
        optional_fields = ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'country',
                           'phone']
        users_api.payload.remove_fields(optional_fields)
        response = users_api.create_user()
        assert response.status_code == 201
        for field in optional_fields:
            assert response.json().get(field) is None

    @m.it("Verify able to create user successfully")
    def test_able_to_create_user(self, users_api):
        sent_data = users_api.payload
        post_response = users_api.create_user()
        assert post_response.status_code == 201
        created_user = post_response.json()

        assert_that(created_user).contains('id')
        assert_that(created_user['email']).is_equal_to(sent_data.email)
        assert_that(created_user).does_not_contain('password')
        assert_that(created_user).does_not_contain('confirm_password')
        assert_that(created_user['first_name']).is_equal_to(sent_data.first_name)
        assert_that(created_user['last_name']).is_equal_to(sent_data.last_name)
        assert_that(created_user['address_1']).is_equal_to(sent_data.address_1)
        assert_that(created_user['address_2']).is_equal_to(sent_data.address_2)
        assert_that(created_user['city']).is_equal_to(sent_data.city)
        assert_that(created_user['state']).is_equal_to(sent_data.state)
        assert_that(created_user['country']).is_equal_to(sent_data.country)
        assert_that(created_user['zip_code']).is_equal_to(sent_data.zip_code)
        assert_that(created_user['country']).is_equal_to(sent_data.country)
        assert_that(created_user['phone']).is_equal_to(sent_data.phone)
        assert_that(created_user['user_level']).is_equal_to(sent_data.user_level)
        assert_that(created_user).contains('created_at_utc')

    @m.it("Verify all fields accept max length values")
    def test_user_max_length_values_accepted(self, users_api):
        users_api.payload.email = '{}@gmail.com'.format(random_string(240))

        users_api.payload.password = random_string(128)
        users_api.payload.confirm_password = users_api.payload.password

        users_api.payload.first_name = random_string(128)
        users_api.payload.last_name = random_string(128)
        users_api.payload.address_1 = random_string(250)
        users_api.payload.address_2 = random_string(250)
        users_api.payload.city = random_string(80)
        users_api.payload.state = random_string(80)
        users_api.payload.zip_code = random_string(20)
        users_api.payload.country = random_string(80)
        users_api.payload.phone = random_string(80)

        sent_data = users_api.payload
        post_response = users_api.create_user()
        assert post_response.status_code == 201

        get_response = users_api.get_user(post_response.json()['id'])
        assert get_response.status_code == 200

        created_user = get_response.json()

        assert_that(created_user['email']).is_equal_to(sent_data.email)
        assert_that(created_user['first_name']).is_equal_to(sent_data.first_name)
        assert_that(created_user['last_name']).is_equal_to(sent_data.last_name)
        assert_that(created_user['address_1']).is_equal_to(sent_data.address_1)
        assert_that(created_user['address_2']).is_equal_to(sent_data.address_2)
        assert_that(created_user['city']).is_equal_to(sent_data.city)
        assert_that(created_user['state']).is_equal_to(sent_data.state)
        assert_that(created_user['country']).is_equal_to(sent_data.country)
        assert_that(created_user['zip_code']).is_equal_to(sent_data.zip_code)
        assert_that(created_user['country']).is_equal_to(sent_data.country)
        assert_that(created_user['phone']).is_equal_to(sent_data.phone)

    max_length_exceed_cases = [
        ("email", '{}@gmail.com'.format(random_string(241)), "Length must be between 1 and 250."),
        ("confirm_password", random_string(129), "Length must be between 1 and 128."),
        ("password", random_string(129), "Length must be between 1 and 128."),
        ("first_name", random_string(129), "Longer than maximum length 128."),
        ("last_name", random_string(129), "Longer than maximum length 128."),
        ("address_1", random_string(251), "Longer than maximum length 250."),
        ("address_2", random_string(251), "Longer than maximum length 250."),
        ("city", random_string(81), "Longer than maximum length 80."),
        ("state", random_string(81), "Longer than maximum length 80."),
        ("zip_code", random_string(21), "Longer than maximum length 20."),
        ("country", random_string(81), "Longer than maximum length 80."),
        ("phone", random_string(129), "Longer than maximum length 80.")]

    @pytest.mark.parametrize("field, value, message", max_length_exceed_cases)
    @m.it("Verify all fields reject values longer than max length")
    def test_user_max_length_values_rejected(self, field, value, message, users_api):
        setattr(users_api.payload, field, value)
        response = users_api.create_user()
        assert response.status_code == 400
        assert response.json()['message'][field][0] == message


@m.describe("Update User")
class TestUpdateUser:

    @m.it("Verify required field error is returned if email is skipped")
    def test_email_is_required_if_skipped(self, users_api):
        user = users_api.create_user()
        users_api.payload.remove_field('email')
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['email'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if email == empty string")
    def test_email_is_required_if_empty_string(self, users_api):
        user = users_api.create_user()
        users_api.payload.email = ''
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert_that(response.json()['message']['email']).contains('Not a valid email address.')
        assert_that(response.json()['message']['email']).contains('Length must be between 1 and 250.')

    @m.it("Verify only valid email values are accepted")
    @pytest.mark.parametrize("case, email", max_length_exceed_cases)
    def test_email_format_is_validated(self, case, email, users_api):
        print(colored("\n\nRunning test_framework case: {}".format(case), color='yellow'))
        user = users_api.create_user()
        users_api.payload.email = email
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['email'][0] == 'Not a valid email address.'
        print("\nTest case: {} {}".format(case, colored('PASSED', 'green')))

    @m.it("Verify email is unique")
    def test_email_is_unique(self, users_api):
        response1 = users_api.create_user()
        assert response1.status_code == 201
        response2 = UsersAPI(debug=True).create_user()
        assert response2.status_code == 201
        users_api.payload.email = response2.json()['email']
        response3 = users_api.update_user(response1.json()['id'])
        assert response3.status_code == 400
        assert response3.json()['message'] == "user.email already exists"

    @m.it("Verify email is lowercased before storing in the DB")
    def test_email_is_lowercased(self, users_api):
        user = users_api.create_user()
        email = "MYEMAIL+" + random_string(6) + "@gmail.com"
        users_api.payload.email = email
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 200
        assert response.json()['email'] == email.lower()

    @m.it("Verify required field error is returned if password is skipped")
    def test_password_is_required_skipped(self, users_api):
        user = users_api.create_user()
        users_api.payload.remove_field('password')
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['password'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if password == empty string")
    def test_password_is_required_if_empty_string(self, users_api):
        user = users_api.create_user()
        users_api.payload.password = ''
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert_that(response.json()['message']['password']).contains('Length must be between 1 and 128.')

    @m.it("Verify required field error is returned if confirm_password is skipped")
    def test_confirm_password_is_required_if_skipped(self, users_api):
        user = users_api.create_user()
        users_api.payload.remove_field('confirm_password')
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['confirm_password'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if confirm_password == empty string")
    def test_confirm_password_is_required_if_empty_string(self, users_api):
        user = users_api.create_user()
        users_api.payload.confirm_password = ''
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert_that(response.json()['message']['confirm_password']).contains('Length must be between 1 and 128.')

    @m.it("Verify required field error is returned if user_level is skipped")
    def test_user_level_is_required_if_skipped(self, users_api):
        user = users_api.create_user()
        users_api.payload.remove_field('user_level')
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['user_level'][0] == 'Missing data for required field.'

    @m.it("Verify required field error is returned if user_level == empty string")
    def test_user_level_is_required_if_empty_string(self, users_api):
        user = users_api.create_user()
        users_api.payload.user_level = ''
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert_that(response.json()['message']['user_level']).contains('Must be one of: admin, user.')

    @m.it("Verify user_level field accepts value 'admin'")
    def test_user_level_accepts_admin_value(self, users_api):
        user = users_api.create_user()
        users_api.payload.user_level = 'admin'
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 200
        assert response.json()['user_level'] == 'admin'

    @m.it("Verify user_level field accepts value 'user'")
    def test_user_level_accepts_user_value(self, users_api):
        user = users_api.create_user()
        users_api.payload.user_level = 'user'
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 200
        assert response.json()['user_level'] == 'user'

    @m.it("Verify user_level field rejects values different from ['admin', 'user']")
    def test_user_level_rejects_random_values(self, users_api):
        user = users_api.create_user()
        users_api.payload.user_level = 'someone'
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 400
        assert response.json()['message']['user_level'][0] == 'Must be one of: admin, user.'

    @m.it("Verify user_level is lowercased before storing in the DB")
    def test_user_level_is_lowercased(self, users_api):
        user = users_api.create_user()
        users_api.payload.user_level = 'ADMIN'
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 200
        assert response.json()['user_level'] == 'admin'

    @m.it("Verify able to update a user without providing optional fields")
    def test_optional_fields(self, users_api):
        user = users_api.create_user()
        optional_fields = ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'country',
                           'phone']
        users_api.payload.remove_fields(optional_fields)
        response = users_api.update_user(user.json()['id'])
        assert response.status_code == 200

    @m.it("Verify able to update all fields successfully")
    def test_able_to_update_user(self, users_api):
        user = users_api.create_user()
        users_api.payload.email = "myemail+" + random_string(6) + "@gmail.com"
        users_api.payload.password = 'MyPassword9900'
        users_api.payload.confirm_password = 'MyPassword9900'
        users_api.payload.first_name = 'John'
        users_api.payload.last_name = 'Doe'
        users_api.payload.address_1 = 'Charleston 87'
        users_api.payload.address_2 = 'St 88'
        users_api.payload.city = 'Austin'
        users_api.payload.state = 'Texas'
        users_api.payload.zip_code = '88769'
        users_api.payload.country = 'USA'
        users_api.payload.phone = '111222333'
        users_api.payload.user_level = 'user'

        sent_data = users_api.payload

        update_response = users_api.update_user(user.json()['id'])
        assert update_response.status_code == 200
        get_user = users_api.get_user(user.json()['id'])
        updated_user = get_user.json()

        assert_that(updated_user).contains('id')
        assert_that(updated_user['email']).is_equal_to(sent_data.email)
        assert_that(updated_user).does_not_contain('password')
        assert_that(updated_user).does_not_contain('confirm_password')
        assert_that(updated_user['first_name']).is_equal_to(sent_data.first_name)
        assert_that(updated_user['last_name']).is_equal_to(sent_data.last_name)
        assert_that(updated_user['address_1']).is_equal_to(sent_data.address_1)
        assert_that(updated_user['address_2']).is_equal_to(sent_data.address_2)
        assert_that(updated_user['city']).is_equal_to(sent_data.city)
        assert_that(updated_user['state']).is_equal_to(sent_data.state)
        assert_that(updated_user['country']).is_equal_to(sent_data.country)
        assert_that(updated_user['zip_code']).is_equal_to(sent_data.zip_code)
        assert_that(updated_user['country']).is_equal_to(sent_data.country)
        assert_that(updated_user['phone']).is_equal_to(sent_data.phone)
        assert_that(updated_user['user_level']).is_equal_to(sent_data.user_level)
        assert_that(updated_user).contains('created_at_utc')

    @m.it("Verify all fields accept max length values")
    def test_user_max_length_values_accepted(self, users_api):
        post_response = users_api.create_user()
        assert post_response.status_code == 201

        users_api.payload.email = '{}@gmail.com'.format(random_string(240))
        users_api.payload.password = random_string(128)
        users_api.payload.confirm_password = users_api.payload.password
        users_api.payload.first_name = random_string(128)
        users_api.payload.last_name = random_string(128)
        users_api.payload.address_1 = random_string(250)
        users_api.payload.address_2 = random_string(250)
        users_api.payload.city = random_string(80)
        users_api.payload.state = random_string(80)
        users_api.payload.zip_code = random_string(20)
        users_api.payload.country = random_string(80)
        users_api.payload.phone = random_string(80)

        sent_data = users_api.payload

        update_response = users_api.update_user(post_response.json()['id'])
        assert update_response.status_code == 200

        get_response = users_api.get_user(post_response.json()['id'])
        assert get_response.status_code == 200

        updated_user = get_response.json()

        assert_that(updated_user['email']).is_equal_to(sent_data.email)
        assert_that(updated_user['first_name']).is_equal_to(sent_data.first_name)
        assert_that(updated_user['last_name']).is_equal_to(sent_data.last_name)
        assert_that(updated_user['address_1']).is_equal_to(sent_data.address_1)
        assert_that(updated_user['address_2']).is_equal_to(sent_data.address_2)
        assert_that(updated_user['city']).is_equal_to(sent_data.city)
        assert_that(updated_user['state']).is_equal_to(sent_data.state)
        assert_that(updated_user['country']).is_equal_to(sent_data.country)
        assert_that(updated_user['zip_code']).is_equal_to(sent_data.zip_code)
        assert_that(updated_user['country']).is_equal_to(sent_data.country)
        assert_that(updated_user['phone']).is_equal_to(sent_data.phone)

    max_length_exceed_cases = [
        ("email", '{}@gmail.com'.format(random_string(241)), "Length must be between 1 and 250."),
        ("confirm_password", random_string(129), "Length must be between 1 and 128."),
        ("password", random_string(129), "Length must be between 1 and 128."),
        ("first_name", random_string(129), "Longer than maximum length 128."),
        ("last_name", random_string(129), "Longer than maximum length 128."),
        ("address_1", random_string(251), "Longer than maximum length 250."),
        ("address_2", random_string(251), "Longer than maximum length 250."),
        ("city", random_string(81), "Longer than maximum length 80."),
        ("state", random_string(81), "Longer than maximum length 80."),
        ("zip_code", random_string(21), "Longer than maximum length 20."),
        ("country", random_string(81), "Longer than maximum length 80."),
        ("phone", random_string(129), "Longer than maximum length 80.")]

    @pytest.mark.parametrize("field, value, message", max_length_exceed_cases)
    @m.it("Verify all fields reject values longer than max length")
    def test_user_max_length_values_rejected(self, field, value, message, users_api):
        post_response = users_api.create_user()
        setattr(users_api.payload, field, value)
        put_response = users_api.update_user(post_response.json()['id'])
        assert put_response.status_code == 400
        assert put_response.json()['message'][field][0] == message


@m.describe("Get User")
class TestGetUser:

    @m.it("Verify 'Not Found' error is returned when trying to get non-existing user")
    def test_get_non_existing_user(self, users_api):
        response = users_api.get(19999999)
        assert response.status_code == 404
        assert response.json()['message'] == 'User not found.'

    @m.it("Verify all correct values are returned for all fields")
    def test_get_one_user(self, users_api):
        """Create a user, get and verify all fields"""
        sent_data = users_api.payload
        post_response = users_api.create_user()
        assert post_response.status_code == 201

        get_response = users_api.get_user(post_response.json()['id'])
        assert get_response.status_code == 200

        get_user = get_response.json()

        assert_that(get_user).contains('id')
        assert_that(get_user['email']).is_equal_to(sent_data.email)
        assert_that(get_user).does_not_contain('password')
        assert_that(get_user).does_not_contain('confirm_password')
        assert_that(get_user['first_name']).is_equal_to(sent_data.first_name)
        assert_that(get_user['last_name']).is_equal_to(sent_data.last_name)
        assert_that(get_user['address_1']).is_equal_to(sent_data.address_1)
        assert_that(get_user['address_2']).is_equal_to(sent_data.address_2)
        assert_that(get_user['city']).is_equal_to(sent_data.city)
        assert_that(get_user['state']).is_equal_to(sent_data.state)
        assert_that(get_user['country']).is_equal_to(sent_data.country)
        assert_that(get_user['zip_code']).is_equal_to(sent_data.zip_code)
        assert_that(get_user['country']).is_equal_to(sent_data.country)
        assert_that(get_user['phone']).is_equal_to(sent_data.phone)
        assert_that(get_user['user_level']).is_equal_to(sent_data.user_level)
        assert_that(get_user).contains('created_at_utc')

    def test_get_all_users(self, users_api):
        """Create 3 users in case DB is empty, get number of users in DB and compare with returned list number"""
        # TODO runs with Pycharm runner, fails from terminal
        UsersAPI().create_user()
        UsersAPI().create_user()
        UsersAPI().create_user()

        sql = 'SELECT * FROM user'
        all_db_users = run_db_query('data.sqlite', sql)

        get_response = users_api.get_users()
        assert get_response.status_code == 200
        assert len(get_response.json()) == len(all_db_users)


@m.describe("Delete User")
class TestDeleteUser:
    @m.it("Verify 'Not Found' error is returned when trying to delete non-existing user")
    def test_delete_non_existing_user(self, users_api):
        response = users_api.delete_user(19999999)
        assert response.status_code == 404
        assert response.json()['message'] == 'User not found.'

    @m.it("Verify able to delete user successfully")
    def test_delete_user(self, users_api):
        """Create a user and delete"""
        create_response = users_api.create_user()
        assert create_response.status_code == 201

        delete_response = users_api.delete_user(create_response.json()['id'])
        assert delete_response.status_code == 200
        assert delete_response.json()['message'] == 'User deleted'
        # TODO using users_api vs UsersAPI(debug=True)
        get_response = UsersAPI(debug=True).get_user(create_response.json()['id'])
        assert get_response.status_code == 404
        assert get_response.json()['message'] == 'User not found.'

# TODO Questions
# 1. when creating user, is it worth to check all fields are stored in the DB ?
# 2. when getting  all users, is it worth to check values for all or only length is ok ?
# 3, when checking GET not found, should I create-delete-get, or get very big ID is ok ? Also should I check response model -
# e.g. passwords hidden, created_date returned
# 4. using users_api fixture for a few actions vs using UsersAPI(). Should I use same object for different calls or create one for each action ?
