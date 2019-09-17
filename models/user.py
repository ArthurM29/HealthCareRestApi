from marshmallow import post_load, ValidationError, validate, fields

from db import db, ma
from models.base import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    __tablename__ = 'user'

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

    @classmethod
    def find_by_email(cls, email):
        """Find the model by email"""
        return cls.query.filter_by(email=email).first()


class UserSchema(ma.ModelSchema):
    # additional validation in schema level
    email = fields.Email(validate=validate.Length(max=250), required=True)
    confirm_password = fields.String(validate=validate.Length(max=128), required=True)
    user_level = fields.Str(validate=validate.OneOf(["admin", "user"]), required=True)

    class Meta:
        model = UserModel
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
