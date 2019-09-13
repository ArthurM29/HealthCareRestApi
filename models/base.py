from marshmallow import ValidationError

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
    def find_by(cls, **kwargs):
        #TODO do I need this ?
        return cls.query.filter_by(kwargs).first()

    def get_from_db(self, *args):
        pass

    @classmethod
    def validate(cls, *args, **kwargs):
        pass

    def store_path_param(self, path_id):
        pass

    @classmethod
    def unique_field(cls, data, field, id=None):
        field_to_update = data[field]

        # method = put
        if id:
            item = cls.find_by_id(id)
            d = {field: field_to_update}
            value_exists_in_db = bool(cls.find_by(d))
            new_field_is_different = getattr(item, field) != field_to_update

            if new_field_is_different and value_exists_in_db:
                raise ValidationError("Another {} is registered with name '{}'.".format(cls.__tablename__, field_to_update),
                                      field_name=field)

        # method = post
        elif cls.find_by_name(field_to_update):
            # TODO this doesn't work, probably because of using flask-marshmallow
            raise ValidationError("{} with name '{}' already exists.".format(cls.__tablename__.title(), field_to_update), field_name=field)

        return field_to_update
