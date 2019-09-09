from flask_restful import Resource, abort, request
from marshmallow import ValidationError


class BaseResource(Resource):
    name = ''
    model = None

    def get(self, id=None):
        """Retrieve all items from DB."""
        if not id:
            items = self.model.query.all()
            return [item.json() for item in items]

        item = self.model.find_by_id(id)

        if item:
            return item

        abort(404, message='{} not found.'.format(self.name.title()))

    def post(self):
        """Create a new item."""
        raw_data = request.get_json(force=True)

        try:
            data = self.model.schema().load(raw_data)
            item = self.model(**data)
            item.validate(raw_data)
        except ValidationError as err:
            abort(400, message=err.messages)

        item.save_to_db()
        return item, 201, {'Location': request.url + '/' + str(item.id)}

    def put(self, id):
        """Update item by id."""
        item = self.model.find_by_id(id)

        if item:
            raw_data = request.get_json(force=True)
            data = self.model.schema().load(raw_data)

            try:
                self.model.validate(data, id)
            except ValidationError as err:
                abort(400, message=err.messages)

            item.update(data)
            item.save_to_db()
            return item

        abort(404, message='{} not found.'.format(self.name.title()))

    def delete(self, id):
        """Delete item by id."""
        item = self.model.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': '{} deleted'.format(self.name.title())}

        abort(404, message='{} not found.'.format(self.name.title()))

    def validate(self, raw_data, method, id=None):
        return True
        # method = put
        if id:
            item = cls.find_by_id(id)
            if item:
                existing_user = True
            else:
                existing_user = False

            email_is_not_unique = cls.find_by_email(raw_data['email'])

            if existing_user:
                if email_is_not_unique and item.email != raw_data['email']:
                    raise ValidationError("Another user is registered with email '{}'.".format(raw_data['email']))

        # method = post
        if cls.find_by_email(raw_data['email']):
            raise ValidationError("User with email '{}' already exists.".format(raw_data['email']))
