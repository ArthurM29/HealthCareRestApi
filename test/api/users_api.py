from test.api.api_call import ApiCall
from test.config.config import URL


class CreateUsersAPI(ApiCall):
    """Creates a new user"""
    path = URL.USERS_ROUTE

    def __init__(self, headers=None, payload=None, **kwargs):
        if headers is None:
            self.headers = {'content-type': 'application/json', 'accept': 'application/json'}
        else:
            self.headers = headers
        super().__init__(method='post', headers=self.headers, payload=payload, **kwargs)
