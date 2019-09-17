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
    def get_from_db(cls, parent_field=None, parent_id=None, self_id=None):
        # routes with parent_id
        if parent_id:
            if self_id:
                return cls.query.filter(parent_field == parent_id, cls.id == self_id).first()
            else:
                return cls.query.filter(parent_field == parent_id).all()
        # routes without parent_id
        else:
            if self_id:
                return cls.query.filter(cls.id == self_id).first()
            else:
                return cls.query.filter().all()

    @classmethod
    def validate(cls, *args, **kwargs):
        """Handle any validation in data"""
        pass

    def set_parent_id(self, parent_id):
        """Set parent id from path parameter in model"""
        pass
