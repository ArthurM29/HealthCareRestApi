from flask import Flask
from flask_restful import Api

from resources.user import User
from resources.organization import Organization


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turn off Flask-SQLAlchemy modification tracker and leave SQLAlchemy tracker
app.config['BUNDLE_ERRORS'] = True   # show all errors handled by the RequestParser together


api.add_resource(User, '/users', endpoint='users')
api.add_resource(User, '/users/<string:id>', endpoint='user')
api.add_resource(Organization, '/organizations', endpoint='organizations')
api.add_resource(Organization, '/organizations/<string:id>', endpoint='organization')


if __name__ == '__main__':
    from db import db, ma

    db.init_app(app)
    ma.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(debug=True)





#TODO is it worth to handle exceptions for all db actions and return 500 ?
#  TODO consder using first_or_404 or get_or_404 methods
# notes
# * IDs should be opaque, globally unique, avoid sequential numbers, use uuids
# *