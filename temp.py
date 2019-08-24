from db import db
from models.user import UserModel

user = UserModel.query()
print(type(user))