from test_framework.api.api_call import ApiCall
from test_framework.config.config import URL
from test_framework.models.UserModel import UserModel


class UsersAPI(ApiCall):
    path = URL.USERS_ROUTE

    def __init__(self, headers=None, payload=None, query_params=None, debug=False, **kwargs):
        if headers is None:
            self.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        else:
            self.headers = headers

        if payload is None:
            self.payload = UserModel()
        else:
            self.payload = payload

        super().__init__(headers=self.headers, payload=self.payload, query_params=query_params, debug=debug,
                         kwargs=kwargs)

    def create_user(self):
        #TODO maybe this should return User object ?
        return self.post()

    def get_user(self, id_):
        return self.get(id_)

    def get_users(self):
        return self.get()

    def update_user(self, id_=None):
        return self.put(id_)

    def delete_user(self, id_=None):
        return self.delete(id_)
