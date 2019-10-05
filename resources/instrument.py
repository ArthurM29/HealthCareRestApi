from random import randrange
import time
import threading
from flask import copy_current_request_context

from sqlalchemy.exc import IntegrityError
from flask_restful import abort, request
from marshmallow import ValidationError
from common.utils import random_string

from models.instrument import InstrumentModel, InstrumentSchema
from resources.base import BaseResource


class Instrument(BaseResource):
    name = 'instrument'
    model = InstrumentModel
    schema = InstrumentSchema

    def post(self, parent_id=None):
        """Create a new item."""
        if parent_id:
            self.verify_parent_id_exists(parent_id)

        raw_data = request.get_json(force=True)

        try:
            item = self.schema().load(raw_data)
            item.validate(raw_data)

            # to pass Flask application context to the thread
            @copy_current_request_context
            def set_pairing_code(item_):
                time.sleep(randrange(2, 9))  # [2, 8]
                item_.pairing_code = random_string(8, charset='1234567890')
                item_.save_to_db()

            # set pairing_code in separate thread to simulate asynchronous execution with delay
            thread = threading.Thread(target=set_pairing_code, args=(item,))
            thread.start()

            item.set_parent_id(parent_id)
            item.save_to_db()

        except ValidationError as err:
            abort(400, message=err.messages)
        except IntegrityError as err:
            self.handle_db_integrity_errors(err)

        return self.json(item), 201, {'Location': request.url + '/' + str(item.id)}

    def put(self, **kwargs):
        abort(405)

    def delete(self, **kwargs):
        abort(405)
