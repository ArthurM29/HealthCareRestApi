# from test.models.UserModel import UserModel
# from test.api.users_api import UsersAPI
#
# h = {"content": "application/xml"}
#
# user = UserModel()
# users_api = UsersAPI(payload=user.json(), headers=h, debug=True)
# create_resp = users_api.create_user()
# print(create_resp)
#
# get_resp = users_api.get_user(create_resp.json()['id'])
# print(get_resp.text)


# class Temperature:
#     def __init__(self, temp):
#         self._temperature = temp
#
#     @property
#     def temperature(self):
#         print("Getting value")
#         return float(self._temperature)
#
#     @temperature.setter
#     def temperature(self, val):
#         print("Setting value")
#         self._temperature = val
#
#     def check_temp(self):
#         print(self._temperature)
#
#
# t = Temperature(44)
# print(t.temperature)
#
# t.temperature = 33
# print(t.temperature)
#
# t.check_temp()


import urllib.parse

BASE_URL = 'http://127.0.0.1:5000'
USERS_ROUTE = '/users'
USERS_ID_ROUTE = '/users/{id}'


id = 11

url = urllib.parse.urljoin(BASE_URL, USERS_ROUTE).format(id=id)
print(url)
print('Hello '.format('world'))