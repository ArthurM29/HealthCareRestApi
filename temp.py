# import datetime as dt
# from marshmallow import Schema, fields, pprint, post_load, validate, EXCLUDE, ValidationError, pre_load
# from models.user import UserModel
#
#
# class UserSchema(Schema):
#     email = fields.Email(validate=validate.Length(max=250), required=True)
#     password = fields.String(validate=validate.Length(max=128), required=True, load_only=True)
#     first_name = fields.String(validate=validate.Length(max=128))
#     last_name = fields.String(validate=validate.Length(max=128))
#     address_1 = fields.String(validate=validate.Length(max=128))
#     address_2 = fields.String(validate=validate.Length(max=128))
#     city = fields.String(validate=validate.Length(max=80))
#     state = fields.String(validate=validate.Length(max=80))
#     zip_code = fields.String(validate=validate.Length(max=80))
#     country = fields.String(validate=validate.Length(max=80))
#     phone = fields.String(validate=validate.Length(max=80))
#     user_level = fields.String(validate=validate.Length(max=80))
#     created_at_utc = fields.DateTime()
#
#     class Meta:
#         # exclude = ["password"]
#         datetimeformat = ''
#         ordered = True
#         # unknown = EXCLUDE
#
#     @post_load
#     def make_user(self, data, **kwargs):
#         return UserModel(**data)
#
#     @pre_load
#     def compare_passwords(self, data, **kwargs):
#         if not data.get('confirm_password'):
#             raise ValidationError("Confirm_password is a required field")
#         if data['confirm_password'] != data['password']:
#             raise ValidationError("Passwords do not match")
#         new_data = {k: v for k, v in data.items() if k != 'confirm_password'}
#         return new_data
#
#
# user_data = {
#     "email": "ar2mac.com",
#     "password": "Pass",
#     "confirm_password": "Pass",
#     "first_name": "Arthur",
#     "last_name": "Manasyan",
#     "address_1": "Komitas 8, 50",
#     "address_2": "",
#     "city": "Yerevan",
#     "state": "",
#     "zip_code": "0033",
#     "country": "Armenia",
#     "phone": "271219"
# }
#
# schema = UserSchema()
# user = schema.load(user_data)
# pprint(schema.dump(user))
#
# # user = UserModel(email='arthur@mac.com', password='aaa')
# # pprint(schema.dump(user.json()))


# data = {
#     "email": "myemail@gmail.com",
#     "password": "Pass",
#     "confirm_password": "Pass",
#     "first_name": "Arthur",
#     "last_name": "Manasyan",
#     "address_1": "Komitas 8, 50",
#     "address_2": "Barekamutyun",
#     "city": "Yerevan",
#     "state": "N/A",
#     "zip_code": "0033",
#     "country": "Armenia",
#     "phone": "271219",
#     "user_level": "admin"
# }
#
# data2 = dict(data)
# data2['email'] = '222'
# print(data)
# print(data2)
from common.utils import random_string

from faker import Faker

fake = Faker()
for i in range(10):
    print(random_string(6))