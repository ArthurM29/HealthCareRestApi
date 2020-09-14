from datetime import datetime

from marshmallow import ValidationError, fields, validate, pre_load

from db import db, ma
from models.base import BaseModel
from models.clinic import ClinicModel


class PatientModel(BaseModel):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    passport = db.Column(db.String(80), nullable=False, unique=True)
    insurance_number = db.Column(db.String(80))
    age = db.Column(db.Integer())
    sex = db.Column(db.String(20), nullable=False)
    medical_condition = db.Column(db.String(512))
    email = db.Column(db.String(250))
    address_1 = db.Column(db.String(250))
    address_2 = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    clinic = db.relationship('ClinicModel', backref='PatientModel', lazy=True)

    @staticmethod
    def parent_id_exists(path_id):
        """Check if clinic with id=path_id exists in the DB"""
        if not ClinicModel.find_by_id(path_id):
            raise ValidationError('Clinic with id={} does not exist.'.format(path_id))

    def set_parent_id(self, parent_id):
        self.clinic_id = parent_id

    @classmethod
    def get_from_db(cls, parent_field=None, parent_id=None, self_id=None):
        return super().get_from_db(cls.clinic_id, parent_id, self_id)


class PatientSchema(ma.SQLAlchemyAutoSchema):
    # additional validation in schema level
    first_name = fields.String(validate=validate.Length(min=1, max=250), required=True)
    last_name = fields.String(validate=validate.Length(min=1, max=250), required=True)
    passport = fields.String(validate=validate.Length(min=1, max=80), required=True)
    date_of_birth = fields.DateTime(format='%d-%m-%Y', required=True)
    sex = fields.Str(validate=validate.OneOf(["male", "female"]), required=True)
    email = fields.Email(validate=validate.Length(min=1, max=250))

    class Meta:
        model = PatientModel
        ordered = True
        load_only = ['clinic']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def lower_case_fields(self, data, **kwargs):
        if data.get('sex'):
            data['sex'] = data['sex'].lower().strip()
        if data.get('email'):
            data['email'] = data['email'].lower().strip()
        return data





