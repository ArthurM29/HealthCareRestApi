from db import db
from models.base_model import BaseModel


class OrganizationModel(BaseModel):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    address_1 = db.Column(db.String(250))
    address_2 = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('UserModel', backref='OrganizationModel', lazy=True)
