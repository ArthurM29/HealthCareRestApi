from models.clinic import ClinicModel, ClinicSchema
from resources.base import BaseResource


class Clinic(BaseResource):
    name = 'clinic'
    model = ClinicModel
    schema = ClinicSchema



