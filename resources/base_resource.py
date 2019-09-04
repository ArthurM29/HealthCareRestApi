from flask_restful import Resource, abort, request
from marshmallow import ValidationError


class BaseResource(Resource):
    model = None

    def get(self, id=None):
        """Retrieve all items from DB."""
        if not id:
            items = self.model.query.all()
            return [item.json() for item in items]

        item = self.model.find_by_id(id)

        if item:
            schema = item.schema()
            a = schema.dump(item)
            return a

        abort(404, message='Item not found.')

    def post(self):
        """Create a new item."""
        data = request.get_json(force=True)
        try:
            item = self.model.schema().load(data)
        except ValidationError as err:
            abort(400, message=err.messages)

        item.save_to_db()
        return item.json(), 201, {'Location': request.url + '/' + str(item.id)}

    def put(self, id):
        """Update item by id."""
        data = self.parser.parse_args(strict=True)  # return 400 if unexpected arguments received

        # if UserModel.find_by_email(data['email']) and data['email'] != item.email:
        #     abort(400, message="User with email '{}' already exists.".format(data['email']))

        item = self.model.find_by_id(id)

        if item:
            data = self.validate_arguments()
            item.update(data)
            item.save_to_db()
            return item.json()

        abort(404, message='Item not found.')

    def delete(self, id):
        """Delete item by id."""
        item = self.model.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

        abort(404, message='Item not found.')
