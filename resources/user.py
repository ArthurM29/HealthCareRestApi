from models.user import UserModel, UserSchema
from resources.base_resource import BaseResource


class User(BaseResource):
    name = 'user'
    model = UserModel
    schema = UserSchema
