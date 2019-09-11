from db import db


class BaseModel(db.Model):
    __abstract__ = True  # skip the production of a table or mapper for the class

    def update(self, new_data):
        """Find the model by self.id and update by new_data"""
        self.query.filter_by(id=self.id).update(new_data)

    def save_to_db(self):  # handles both insert and update
        """Save the model to DB"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete the model from DB"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        """Find item by primary key - id"""
        return cls.query.get(id)

    @classmethod
    def validate(cls, *args, **kwargs):
        pass
