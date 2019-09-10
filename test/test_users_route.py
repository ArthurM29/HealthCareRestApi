from test.models.UserModel import UserModel
from test.api.users_api import CreateUsersAPI
from termcolor import colored

from assertpy import assert_that


def test_email_is_required():
    create_user = UserModel()
    delattr(create_user, 'email')
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message']['email'][0] == 'Missing data for required field.'


def test_email_format_is_validated():
    format_validation_cases = {
        "empty_email": "",
        "email_without_local_part": "@mac.com",
        "email_without_@": "myemailmac.com",
        "email_without_middle_part": "myemail@.com",
        "email_without_dot": "myemail@maccom",
        "email_without_domain": "myemail@mac."
    }

    for case, email in format_validation_cases.items():
        print(colored("\n\nRunning test case: {}".format(case), color='yellow'))
        create_user = UserModel()
        create_user.email = email
        create_users_api = CreateUsersAPI(payload=create_user.json())
        create_user_response = create_users_api.call()
        assert create_user_response.status_code == 400
        assert create_user_response.json()['message']['email'][0] == 'Not a valid email address.'
        print("\nTest case: {} {}".format(case, colored('PASSED', 'green')))


def test_email_is_unique():
    create_user = UserModel()
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 201

    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message'][0] == "User with email '{}' already exists.".format(create_user.email)


def test_password_is_required():
    create_user = UserModel()
    delattr(create_user, 'password')
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message']['password'][0] == 'Missing data for required field.'


def test_confirm_password_is_required():
    create_user = UserModel()
    delattr(create_user, 'confirm_password')
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message']['confirm_password'][0] == 'Missing data for required field.'


def test_user_level_is_required():
    create_user = UserModel()
    delattr(create_user, 'user_level')
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message']['user_level'][0] == 'Missing data for required field.'


def test_user_level_accepts_admin_value():
    """Verify user_field accepts value 'admin' """
    create_user = UserModel()
    create_user.user_level = 'admin'
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 201
    assert create_user_response.json()['user_level'] == 'admin'


def test_user_level_accepts_user_value():
    """Verify user_field accepts value 'user']"""
    create_user = UserModel()
    create_user.user_level = 'user'
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 201
    assert create_user_response.json()['user_level'] == 'user'


def test_user_level_rejects_random_values():
    """Verify user_field rejects values different from ['admin', 'user']"""
    create_user = UserModel()
    create_user.user_level = 'someone'
    create_users_api = CreateUsersAPI(payload=create_user.json())
    create_user_response = create_users_api.call()
    assert create_user_response.status_code == 400
    assert create_user_response.json()['message']['user_level'][0] == 'Must be one of: admin, user.'

# def test_optional_fields():
#     """Verify able to create a user without providing optional fields"""
#     create_user = UserModel()
#     create_user.remove_attributes(
#         ['first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'country', 'phone'])
#     create_users_api = CreateUsersAPI(payload=create_user.json())
#     create_user_response = create_users_api.call()
#     assert create_user_response.status_code == 201


# def test_email_is_required():
#     # email = "myemail+{}@gmail.com".format(random_string(6))
#     template_data['email'] = email
#
#     post_response = requests.post(url, json=template_data)
#     assert post_response.status_code == 201
#
#     get_response = requests.get(url + '/' + str(post_response.json()['id']))
#     get_user = get_response.json()
#
#     assert_that(get_response.status_code).is_equal_to(200)
#     assert_that(get_user['email']).is_equal_to(template_data['email'])
#     assert_that(get_user).does_not_contain('password')
#     assert_that(get_user).does_not_contain('confirm_password')
#     assert_that(get_user['first_name']).is_equal_to(template_data['first_name'])
#     assert_that(get_user['last_name']).is_equal_to(template_data['last_name'])
#     assert_that(get_user['address_1']).is_equal_to(template_data['address_1'])
#     assert_that(get_user['address_2']).is_equal_to(template_data['address_2'])
#     assert_that(get_user['city']).is_equal_to(template_data['city'])
#     assert_that(get_user['state']).is_equal_to(template_data['state'])
#     assert_that(get_user['country']).is_equal_to(template_data['country'])
#     assert_that(get_user['zip_code']).is_equal_to(template_data['zip_code'])
#     assert_that(get_user['country']).is_equal_to(template_data['country'])
#     assert_that(get_user['phone']).is_equal_to(template_data['phone'])
#     assert_that(get_user['user_level']).is_equal_to(template_data['user_level'])
#
#     print(json.dumps(get_user, indent=2))
#
#
# def test_able_to_create_user():
#     data = {
#         "email": "myemail+{}@gmail.com".format(random_string(6)),
#         "password": "Pass",
#         "confirm_password": "Pass",
#         "first_name": "Arthur",
#         "last_name": "Manasyan",
#         "address_1": "Komitas 8, 50",
#         "address_2": "Barekamutyun",
#         "city": "Yerevan",
#         "state": "N/A",
#         "zip_code": "0033",
#         "country": "Armenia",
#         "phone": "271219",
#         "user_level": "admin"
#     }
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
