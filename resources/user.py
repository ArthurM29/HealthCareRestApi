from models.user import UserModel, UserSchema
from resources.base import BaseResource


class User(BaseResource):
    name = 'user'
    model = UserModel
    schema = UserSchema
