from datetime import datetime

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
    def parent_id_exists(path_id):
        """Check if organization with id=path_id exists in the DB"""
        if not OrganizationModel.find_by_id(path_id):
            raise ValidationError('Organization with id={} does not exist.'.format(path_id))

    def set_parent_id(self, parent_id):
        self.organization_id = parent_id

    @classmethod
    def get_from_db(cls, parent_field=None, parent_id=None, self_id=None):
        return super().get_from_db(cls.organization_id, parent_id, self_id)


class ClinicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClinicModel
        ordered = True
        load_only = ['organization']
        dump_only = ['id', 'created_at_utc']
        datetimeformat = "%Y-%m-%d %H:%M:%S"
