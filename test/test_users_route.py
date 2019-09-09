import requests, uuid, json
from assertpy import assert_that

url = 'http://127.0.0.1:5000/users'

template_data = {
    "email": "myemail@gmail.com",
    "password": "Pass",
    "confirm_password": "Pass",
    "first_name": "Arthur",
    "last_name": "Manasyan",
    "address_1": "Komitas 8, 50",
    "address_2": "Barekamutyun",
    "city": "Yerevan",
    "state": "N/A",
    "zip_code": "0033",
    "country": "Armenia",
    "phone": "271219",
    "user_level": "admin"
}


def random_string(length):
    """Return parts of UUID"""
    return str(uuid.uuid4())[:length].replace('-', '')


def test_email_is_required():
    data = dict(template_data)
    del data['email']
    print(data)
    post_response = requests.post(url, json=data)
    print(post_response.content)
    assert post_response.status_code == 400
    assert post_response.json()['message']['email'][0] == 'Missing data for required field.'
    print(json.dumps(post_response.json(), indent=2))


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
