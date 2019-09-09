from db import db
from models.base_model import BaseModel
from datetime import datetime
from marshmallow import Schema, fields, post_load, validate, ValidationError, pre_load


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Email(validate=validate.Length(max=250), required=True)
    password = fields.String(validate=validate.Length(max=128), required=True)
    confirm_password = fields.String(validate=validate.Length(max=128), required=True)
    first_name = fields.String(validate=validate.Length(max=128))
    last_name = fields.String(validate=validate.Length(max=128))
    address_1 = fields.String(validate=validate.Length(max=128))
    address_2 = fields.String(validate=validate.Length(max=128))
    city = fields.String(validate=validate.Length(max=80))
    state = fields.String(validate=validate.Length(max=80))
    zip_code = fields.String(validate=validate.Length(max=80))
    country = fields.String(validate=validate.Length(max=80))
    phone = fields.String(validate=validate.Length(max=80))
    user_level = fields.Str(validate=validate.OneOf(["admin", "user"]),
                            required=True)  # TODO should I set a default value here ?
    created_at_utc = fields.DateTime()

    class Meta:
        ordered = True
        load_only = ['password', 'confirm_password']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def create_user(self, data, **kwargs):
        """Get dictionary of deserialized validated data and return UserModel object"""
        data['user_level'] = data['user_level'].lower().strip()
        data['email'] = data['email'].lower().strip()
        if data['confirm_password'] != data['password']:
            raise ValidationError("Passwords do not match", field_name='password')

        data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return data


class UserModel(BaseModel):
    __tablename__ = 'user'
    schema = UserSchema

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    address_1 = db.Column(db.String(250))
    address_2 = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    user_level = db.Column(db.String(20))
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # TODO is it ok to have classmethods or better to create some service layer classes ?
    @classmethod
    def find_by_email(cls, email):
        """Find the model by email"""
        return cls.query.filter_by(email=email).first()

    # @classmethod
    # def validate(cls, raw_data, id=None):
    #     # method = put
    #     if id:
    #         item = cls.find_by_id(id)
    #         if item:
    #             existing_user = True
    #         else:
    #             existing_user = False
    #
    #         email_is_not_unique = cls.find_by_email(raw_data['email'])
    #
    #         if existing_user:
    #             if email_is_not_unique and item.email != raw_data['email']:
    #                 raise ValidationError("Another user is registered with email '{}'.".format(raw_data['email']))
    #
    #     # method = post
    #     if cls.find_by_email(raw_data['email']):
    #         raise ValidationError("User with email '{}' already exists.".format(raw_data['email']))
