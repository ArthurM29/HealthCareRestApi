from datetime import datetime

from flask_restful import abort
from marshmallow import ValidationError

from db import db, ma
from models.base import BaseModel
from models.organization import OrganizationModel


class ClinicModel(BaseModel):
    __tablename__ = 'clinic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(512))
    address_1 = db.Column(db.String(250))
    address_2 = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    organization = db.relationship('OrganizationModel', backref='ClinicModel', lazy=True)

    @classmethod
    def find_by_name(cls, name):
        """Find the model by name"""
        return cls.query.filter_by(name=name).first()

    @staticmethod
    def verify_id(path_id):
        if not OrganizationModel.find_by_id(path_id):
            abort(400, message='Organization does not exist.')

    def store_path_param(self, path_id):
        self.organization_id = path_id

    @classmethod
    def get_from_db(cls, org_id=None, clinic_id=None):
        if org_id:
            return cls.query.filter_by(organization_id=org_id).all()
        else:
            return cls.find_by_id(clinic_id)

    @classmethod
    def validate(cls, data, id=None):
        cls.unique_field(data, 'name', id)


class ClinicSchema(ma.ModelSchema):
    class Meta:
        model = ClinicModel
        ordered = True
        load_only = ['organization']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"
