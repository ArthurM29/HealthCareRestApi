from sqlalchemy.exc import IntegrityError

from flask_restful import Resource, abort, request
from marshmallow import ValidationError


class BaseResource(Resource):
    name = ''
    model = None
    schema = None

    def get(self, parent_id=None, id=None):
        """Retrieve all items from DB."""
        if parent_id:
            self.model.verify_id(parent_id)

        if not id:
            items = self.model.get_from_db(parent_id, id)
            return [self.json(item) for item in items]

        # item = self.model.get_from_db(parent_id, id)
        item = self.model.get_from_db(parent_id, id)

        if item:
            return self.json(item)

        abort(404, message='{} not found.'.format(self.name.title()))

    def post(self, parent_id=None):
        """Create a new item."""
        if parent_id:
            self.model.verify_id(parent_id)

        raw_data = request.get_json(force=True)

        try:
            item = self.schema().load(raw_data)
            # item.validate(raw_data)
        except ValidationError as err:
            abort(400, message=err.messages)

        item.store_path_param(parent_id)
        try:
            item.save_to_db()
        except IntegrityError as err:
            abort(400, message=str(err.orig))

        return self.json(item), 201, {'Location': request.url + '/' + str(item.id)}

    def put(self, id):
        """Update item by id."""
        item = self.model.find_by_id(id)

        if item:
            raw_data = request.get_json(force=True)

            try:
                new_item = self.schema().load(raw_data)
                new_item.validate(raw_data, id)
            except ValidationError as err:
                abort(400, message=err.messages)

            new_data = BaseResource.model_to_dict(new_item)
            try:
                item.update(new_data)
                item.save_to_db()
            except IntegrityError as err:
                abort(400, message=str(err.orig))
            return self.json(item)

        abort(404, message='{} not found.'.format(self.name.title()))

    def delete(self, id):
        """Delete item by id."""
        item = self.model.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': '{} deleted'.format(self.name.title())}

        abort(404, message='{} not found.'.format(self.name.title()))

    def json(self, item):
        return self.schema().dump(item)

    @staticmethod
    def model_to_dict(item):
        # marshmallow-sqlalchemy deserializes to a model object, and there's no way to tell it to return a dictionary
        # this is a known issue: https://github.com/marshmallow-code/marshmallow-sqlalchemy/issues/193

        # workaround: convert Model object to a dictionary
        data = dict(item.__dict__)
        del data['_sa_instance_state']
        return data
