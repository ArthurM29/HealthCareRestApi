from flask import Flask
from flask_restful import Api

from resources.user import UserRegister


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turn off Flask-SQLAlchemy modification tracker and leave SQLAlchemy tracker


api.add_resource(UserRegister, '/users')


if __name__ == '__main__':
    from db import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(debug=True)
