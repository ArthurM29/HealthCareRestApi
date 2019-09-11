from test.models.UserModel import UserModel
from test.api.users_api import UsersAPI

user = UserModel()
users_api = UsersAPI(debug=True)
users_api.payload = user.json()
create_resp = users_api.create()
print(create_resp)

get_resp = users_api.read(12)
print(get_resp.text)


