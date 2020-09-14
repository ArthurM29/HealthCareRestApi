from datetime import datetime

from marshmallow import ValidationError, fields, validate, pre_load

from db import db, ma
from models.base import BaseModel
from models.clinic import ClinicModel


class InstrumentModel(BaseModel):
    __tablename__ = 'instrument'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(512))
    model = db.Column(db.String(80))
    status = db.Column(db.String(80), default='unpaired')
    pairing_code = db.Column(db.String(80), unique=True)
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    clinic = db.relationship('ClinicModel', backref='InstrumentModel', lazy=True)
    
    @classmethod
    def find_by_name(cls, name):
        """Find the model by name"""
        return cls.query.filter_by(name=name).first()

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


class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    # additional validation in schema level
    name = fields.String(validate=validate.Length(min=1, max=250), required=True)

    class Meta:
        model = InstrumentModel
        ordered = True
        load_only = ['clinic']
        dump_only = ['id', 'created_at_utc', 'pairing_code', 'status']
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def lower_case_fields(self, data, **kwargs):
        if data.get('name'):
            data['name'] = data['name'].lower().strip()
        return data
