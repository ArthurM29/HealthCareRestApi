from marshmallow import post_load, ValidationError, validate, fields, pre_load

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
    speciality = db.Column(db.String(250))
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


class UserSchema(ma.SQLAlchemyAutoSchema):
    # additional validation in schema level
    email = fields.Email(validate=validate.Length(min=1, max=250), required=True)
    password = fields.String(validate=validate.Length(min=1, max=128), required=True)
    confirm_password = fields.String(validate=validate.Length(min=1, max=128), required=True)
    user_level = fields.Str(validate=validate.OneOf(["admin", "clinician"]), required=True)

    class Meta:
        model = UserModel
        ordered = True
        load_only = ['password', 'confirm_password']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def lower_case_fields(self, data, **kwargs):
        if data.get('user_level'):
            data['user_level'] = data['user_level'].lower().strip()
        if data.get('email'):
            data['email'] = data['email'].lower().strip()
        return data

    @post_load
    def create_user(self, data, **kwargs):
        """Get dictionary of deserialized validated data and return UserModel object"""
        if data['confirm_password'] != data['password']:
            raise ValidationError("Passwords do not match.", field_name='password')
        if data['user_level'] == 'clinician':
            if not data.get('speciality'):
                raise ValidationError("The field is required for clinicians.", field_name='speciality')

        data = {k: v for k, v in data.items() if k != 'confirm_password'}
        return data
