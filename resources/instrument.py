from models.instrument import InstrumentModel, InstrumentSchema
from resources.base import BaseResource


class Instrument(BaseResource):
    name = 'instrument'
    model = InstrumentModel
    schema = InstrumentSchema
