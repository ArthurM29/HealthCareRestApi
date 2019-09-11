from flask_restful import abort

from models.organization import OrganizationModel, OrganizationSchema
from resources.base import BaseResource


class Organization(BaseResource):
    name = 'organization'
    model = OrganizationModel
    schema = OrganizationSchema

    def delete(self, id):
        abort(405)

# TODO do we need put and delete for this ?
# TODO should I allow to change owner ?
