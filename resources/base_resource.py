from flask_restful import Resource, abort


class BaseResource(Resource):
    name = ''
    model = None

    def get(self, id=None):
        """ Retrieve all items from DB. """
        if not id:
            return {'{}s'.format(self.name): [item.json() for item in self.model.query.all()]}

        item = self.model.find_by_id(id)
        if item:
            return item.json()
        else:
            abort(404, message='{} not found.'.format(self.name.title()))

    def delete(self, id):
        """ Delete item by id. """
        item = self.model.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': '{} deleted'.format(self.name.title())}

        abort(404, message='{} not found.'.format(self.name.title()))
