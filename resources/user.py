from models.user import UserModel
from resources.base_resource import BaseResource


class User(BaseResource):
    model = UserModel
