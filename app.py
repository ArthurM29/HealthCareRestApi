from flask import Flask
from flask_restful import Api

from resources.user import User
from resources.organization import Organization
from resources.clinic import Clinic
from resources.patient import Patient
from resources.instrument import Instrument

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turn off Flask-SQLAlchemy modification tracker and leave SQLAlchemy tracker
app.config['BUNDLE_ERRORS'] = True  # show all errors handled by the RequestParser together

api.add_resource(User, '/users', endpoint='users')
api.add_resource(User, '/users/<string:id>', endpoint='user')
api.add_resource(Organization, '/organizations', endpoint='organizations')
api.add_resource(Organization, '/organizations/<string:id>', endpoint='organization')
api.add_resource(Clinic, '/organizations/<string:parent_id>/clinics', endpoint='clinics')
api.add_resource(Clinic, '/organizations/<string:parent_id>/clinics/<string:id>', endpoint='clinic')
api.add_resource(Patient, '/clinics/<string:parent_id>/patients', endpoint='patients')
api.add_resource(Patient, '/clinics/<string:parent_id>/patients/<string:id>', endpoint='patient')
api.add_resource(Instrument, '/clinics/<string:parent_id>/instruments', endpoint='instruments')
api.add_resource(Instrument, '/clinics/<string:parent_id>/instruments/<string:id>', endpoint='instrument')

if __name__ == '__main__':
    from db import db, ma

    db.init_app(app)
    ma.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(debug=True)
