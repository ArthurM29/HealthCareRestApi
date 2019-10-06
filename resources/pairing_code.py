from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_restful import abort, request

from resources.base import BaseResource
from resources.instrument import InstrumentModel
from models.pairing_code import PairingCodeSchema


class PairingCode(BaseResource):
    """This resource does not have a model"""
    name = 'pairing_code'
    model = None
    schema = PairingCodeSchema

    def post(self, parent_id=None):
        """Pair the instrument."""
        raw_data = request.get_json(force=True)

        try:
            self.schema().load(raw_data)
        except ValidationError as err:
            abort(400, message=err.messages)

        instruments_name = raw_data['instrument_name']
        pairing_code = raw_data['pairing_code']
        instrument = InstrumentModel.find_by_name(instruments_name)

        if not instrument:
            abort(400, message="Instrument with name='{}' does not exist.".format(instruments_name))
        if instrument.status == 'paired':
            abort(400, message="Instrument already paired. You can pair only unpaired instruments.")
        if instrument.pairing_code != pairing_code:
            abort(400, message="Invalid pairing code.")

        try:
            instrument.status = 'paired'
            instrument.save_to_db()
        except IntegrityError as err:
            self.handle_db_integrity_errors(err)

        return {"message": "Instrument paired successfully."}, 201

    def get(self, **kwargs):
        abort(405)

    def put(self, **kwargs):
        abort(405)

    def delete(self, **kwargs):
        abort(405)

    def verify_parent_id_exists(self, parent_id):
        """Check if instrument with id=parent_id exists in the DB"""
        try:
            if not InstrumentModel.find_by_id(parent_id):
                raise ValidationError('Instrument with id={} does not exist.'.format(parent_id))
        except ValidationError as err:
            abort(400, message=err.messages)
