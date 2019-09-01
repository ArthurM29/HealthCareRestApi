from db import db, ma
from models.base_model import BaseModel
from datetime import datetime


class UserSchema(ma.ModelSchema):
    class Meta:
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'address_1',
                  'address_2',
                  'city',
                  'state',
                  'zip_code',
                  'country',
                  'phone',
                  'user_level',
                  'created_at_utc')
        ordered = True


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
    user_level = db.Column(db.String(20))   # TODO define values and add choice validation in parser
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # TODO is it ok to have classmethods or better to create some service layer classes ?
    @classmethod
    def find_by_email(cls, email):
        """Find the model by email"""
        return cls.query.filter_by(email=email).first()
