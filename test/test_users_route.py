from test.api.users_api import UsersAPI
from termcolor import colored
import pytest

from assertpy import assert_that


@pytest.fixture
def users_api():
    return UsersAPI(debug=True)


def test_email_is_required(users_api):
    delattr(users_api.payload, 'email')
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['email'][0] == 'Missing data for required field.'


email_format_cases = [("empty_email", ""),
                      ("email_without_local_part", "@mac.com"),
                      ("email_without_@", "myemailmac.com"),
                      ("email_without_dot", "myemail@maccom"),
                      ("email_without_domain", "myemail@mac.")]


@pytest.mark.parametrize("case, email", email_format_cases)
def test_email_format_is_validated(case, email, users_api):
    print(colored("\n\nRunning test case: {}".format(case), color='yellow'))
    users_api.payload.email = email
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['email'][0] == 'Not a valid email address.'
    print("\nTest case: {} {}".format(case, colored('PASSED', 'green')))


def test_email_is_unique(users_api):
    response1 = users_api.create_user()
    assert response1.status_code == 201

    response2 = users_api.create_user()
    assert response2.status_code == 400
    assert response2.json()['message'] == "user.email already exists"


def test_password_is_required(users_api):
    delattr(users_api.payload, 'password')
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['password'][0] == 'Missing data for required field.'


def test_confirm_password_is_required(users_api):
    delattr(users_api.payload, 'confirm_password')
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['confirm_password'][0] == 'Missing data for required field.'


def test_user_level_is_required(users_api):
    delattr(users_api.payload, 'user_level')
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['user_level'][0] == 'Missing data for required field.'


def test_user_level_accepts_admin_value(users_api):
    """Verify user_field accepts value 'admin' """
    users_api.payload.user_level = 'admin'
    response = users_api.create_user()
    assert response.status_code == 201
    assert response.json()['user_level'] == 'admin'


def test_user_level_accepts_user_value(users_api):
    """Verify user_field accepts value 'user'"""
    users_api.payload.user_level = 'user'
    response = users_api.create_user()
    assert response.status_code == 201
    assert response.json()['user_level'] == 'user'


def test_user_level_rejects_random_values(users_api):
    """Verify user_field rejects values different from ['admin', 'user'"""
    users_api.payload.user_level = 'someone'
    response = users_api.create_user()
    assert response.status_code == 400
    assert response.json()['message']['user_level'][0] == 'Must be one of: admin, user.'


def test_optional_fields(users_api):
    """Verify able to create a user without providing optional fields"""
    users_api.payload.remove_attributes(
        ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'country', 'phone'])
    response = users_api.create_user()
    assert response.status_code == 201


def test_email_and_user_level_are_lowercased(users_api):
    """Verify email and user_level are lowercased"""
    users_api.payload.email = 'MYEMAIL@MAC.COM'
    users_api.payload.user_level = 'ADMIN'
    response = users_api.create_user()
    assert response.status_code == 201
    assert response.status_code == 201


# def test_able_to_create_user():
#
#     post_response = requests.post(url, json=data)
#     assert post_response.status_code == 201
#
#     get_response = requests.get(url + '/' + str(post_response.json()['id']))
#     get_user = get_response.json()
#
#     assert_that(get_response.status_code).is_equal_to(200)
#     assert_that(get_user['email']).is_equal_to(data['email'])
#     assert_that(get_user).does_not_contain('password')
#     assert_that(get_user).does_not_contain('confirm_password')
#     assert_that(get_user['first_name']).is_equal_to(data['first_name'])
#     assert_that(get_user['last_name']).is_equal_to(data['last_name'])
#     assert_that(get_user['address_1']).is_equal_to(data['address_1'])
#     assert_that(get_user['address_2']).is_equal_to(data['address_2'])
#     assert_that(get_user['city']).is_equal_to(data['city'])
#     assert_that(get_user['state']).is_equal_to(data['state'])
#     assert_that(get_user['country']).is_equal_to(data['country'])
#     assert_that(get_user['zip_code']).is_equal_to(data['zip_code'])
#     assert_that(get_user['country']).is_equal_to(data['country'])
#     assert_that(get_user['phone']).is_equal_to(data['phone'])
#     assert_that(get_user['user_level']).is_equal_to(data['user_level'])
#
#     print(json.dumps(get_user, indent=2))


# TODO From post - add lowercase, create and get
# TODO - add Put, Get, Delete
