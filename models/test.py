from datetime import datetime

from marshmallow import ValidationError, fields, validate, pre_load

from db import db, ma
from models.base import BaseModel
from models.patient import PatientModel


class TestModel(BaseModel):
    __tablename__ = 'test'

    # TODO consider adding more fields
    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'), nullable=False)
    instrument = db.relationship('InstrumentModel', backref='TestModel', lazy=True)
    test_type = db.Column(db.String(80), nullable=False)  # TODO define test types with validation
    description = db.Column(db.String(512))
    result = db.Column(db.String(512))
    status = db.Column(db.String(80), default='new')
    created_at_utc = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    patient = db.relationship('PatientModel', backref='TestModel', lazy=True)
    # TODO consider having started_date/completed_date

    @staticmethod
    def parent_id_exists(path_id):
        """Check if patient with id=path_id exists in the DB"""
        if not PatientModel.find_by_id(path_id):
            raise ValidationError('Patient with id={} does not exist.'.format(path_id))

    def set_parent_id(self, parent_id):
        self.patient_id = parent_id

    @classmethod
    def get_from_db(cls, parent_field=None, parent_id=None, self_id=None):
        return super().get_from_db(cls.patient_id, parent_id, self_id)


class TestSchema(ma.ModelSchema):
    # additional validation in schema level
    instrument_id = fields.Integer(required=True)

    class Meta:
        model = TestModel
        ordered = True
        load_only = ['patient', 'instrument']
        dump_only = ['id', 'created_at_utc', 'result', 'status']
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def lower_case_fields(self, data, **kwargs):
        if data.get('test_type'):
            data['test_type'] = data['test_type'].lower().strip()
        return data
