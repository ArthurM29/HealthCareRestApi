from datetime import datetime
from marshmallow import fields, ValidationError

from db import db, ma
from models.base import BaseModel


class OrganizationModel(BaseModel):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
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

    @classmethod
    def validate(cls, data, id=None):
        org_name = data['name']

        # method = put
        if id:
            item = cls.find_by_id(id)
            if item:
                existing_org = True
            else:
                existing_org = False

            org_exists_in_db = bool(cls.find_by_name(org_name))
            new_name_is_different = item.name != org_name

            if existing_org:
                if org_exists_in_db and new_name_is_different:
                    raise ValidationError("Another organization is registered with name '{}'.".format(org_name), field_name='name')

        # method = post
        elif cls.find_by_name(org_name):
            # TODO this doesn't work, probably because of using flask-marshmallow
            raise ValidationError("Organization with name '{}' already exists.".format(org_name), field_name='name')

        return org_name


class OrganizationSchema(ma.ModelSchema):
    # doesn't recognize the field without this
    owner_id = fields.Integer(required=True)

    class Meta:
        model = OrganizationModel
        ordered = True
        load_only = ['owner']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"
