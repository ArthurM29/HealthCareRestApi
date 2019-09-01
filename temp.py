from models.user import UserModel, UserSchema

user = UserModel()
user_schema = UserSchema()
print(user_schema.dump(user))