from models.clinic import ClinicModel, ClinicSchema
from resources.base import BaseResource

from flask_restful import abort


class Clinic(BaseResource):
    name = 'clinic'
    model = ClinicModel
    schema = ClinicSchema

    def delete(self, **kwargs):
        abort(405)
