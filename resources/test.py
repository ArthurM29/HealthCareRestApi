from random import randrange, choice
import time
import threading
from flask import copy_current_request_context

from sqlalchemy.exc import IntegrityError
from flask_restful import abort, request
from marshmallow import ValidationError
from models.instrument import InstrumentModel

from models.test import TestModel, TestSchema
from resources.base import BaseResource


class Test(BaseResource):
    name = 'test'
    model = TestModel
    schema = TestSchema

    def post(self, parent_id=None):
        """Create a new test."""
        if parent_id:
            self.verify_parent_id_exists(parent_id)

        raw_data = request.get_json(force=True)

        instrument = InstrumentModel.find_by_id(raw_data['instrument_id'])
        if not instrument:
            abort(400, message="Instrument with id='{}' does not exist.".format(raw_data['instrument_id']))
        if instrument.status == 'unpaired':
            abort(400, message="Instrument is not paired. You can run tests only on paired instruments.")

        try:
            item = self.schema().load(raw_data)
            item.validate(raw_data)

            # to pass Flask application context to the thread
            @copy_current_request_context
            def generate_test_result(instrument_):
                time.sleep(randrange(2, 9))  # [2, 8]
                instrument_.result = choice(['positive', 'negative'])
                instrument_.status = 'completed'
                instrument_.save_to_db()

            # set test result in separate thread to simulate asynchronous execution with delay
            thread = threading.Thread(target=generate_test_result, args=(item,))
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

    def delete(self, id, parent_id=None):
        """Cancel a test"""
        if parent_id:
            self.verify_parent_id_exists(parent_id)

        test = self.model.get_from_db(parent_id=parent_id, self_id=id)

        if test:
            try:
                test.result = 'cancelled'
                test.save_to_db()
            except IntegrityError as err:
                self.handle_db_integrity_errors(err)

            return {'message': '{} cancelled'.format(self.name.title())}

        abort(404, message='{} not found.'.format(self.name.title()))
