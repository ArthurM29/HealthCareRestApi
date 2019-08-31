from flask_restful import Resource, abort


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
            return item.json()

        abort(404, message='Item not found.')

    def delete(self, id):
        """Delete item by id."""
        item = self.model.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

        abort(404, message='Item not found.')
