from models.user import UserModel
from resources.base_resource import BaseResource


class User(BaseResource):
    name = 'user'
    model = UserModel

    def validate(self, raw_data, method, id=None):
        return True
        # method = put
        if id:
            item = cls.find_by_id(id)
            if item:
                existing_user = True
            else:
                existing_user = False

            email_is_not_unique = cls.find_by_email(raw_data['email'])

            if existing_user:
                if email_is_not_unique and item.email != raw_data['email']:
                    raise ValidationError("Another user is registered with email '{}'.".format(raw_data['email']))

        # method = post
        if cls.find_by_email(raw_data['email']):
            raise ValidationError("User with email '{}' already exists.".format(raw_data['email']))