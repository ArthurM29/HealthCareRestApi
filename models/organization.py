from datetime import datetime
from marshmallow import fields, ValidationError

from db import db, ma
from models.base import BaseModel


class OrganizationModel(BaseModel):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    address_1 = db.Column(db.String(250))
    address_2 = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('UserModel', backref='OrganizationModel', lazy=True)

    @classmethod
    def find_by_name(cls, name):
        """Find the model by name"""
        return cls.query.filter_by(name=name).first()


class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    # doesn't recognize the field without this
    owner_id = fields.Integer(required=True)

    class Meta:
        model = OrganizationModel
        ordered = True
        load_only = ['owner']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"
