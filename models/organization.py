from db import db


class OrganizationModel(db.Model):
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

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, data):
        OrganizationModel.query.filter_by(id=self.id).update(data)

    def save_to_db(self):  # handles both insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)
