from models.patient import PatientModel, PatientSchema
from resources.base import BaseResource

from flask_restful import abort


class Patient(BaseResource):
    name = 'clinic'
    model = PatientModel
    schema = PatientSchema

    def delete(self, **kwargs):
        abort(405)
