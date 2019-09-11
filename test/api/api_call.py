import urllib.parse
import requests
import json
from test.config.config import URL


class ApiCall:
    base_url = URL.BASE_URL
    path = ''

    def __init__(self, method, headers=None, payload=None, query_params=None, **kwargs):
        self.url = urllib.parse.urljoin(self.base_url, self.path)
        self.method = method
        self.headers = headers
        self.payload = payload
        self.query_params = query_params
        self.kwargs = kwargs

    def call(self):
        if self.method:
            self.log_request()
            response = requests.request(self.method, self.url, data=self.payload, headers=self.headers,
                                        params=self.query_params)
            self.log_response(response)
            return response
        else:
            raise Exception('Invalid verb')

    def log_request(self):
        log = f"\n---->Request: {self.method.upper()} {self.url}"
        if self.headers:
            log += f"\nheaders = {self.headers}"
        if self.query_params:
            log += f"\nquery_params = {self.query_params}"
        if self.payload:
            log += f"\npayload = {self.payload}"
        if self.kwargs:
            log += f"\n**kwargs = {self.kwargs}"
        print(log)

    # TODO is this ok, that this method gets response as argument ? Would it be better to store response as state ?
    def log_response(self, response):
        log = f"\n<----Response: \nStatus code: {response.status_code}"
        if response:
            log += f"\nBody: {json.dumps(response.json(), indent=2)}"
        if not response.ok:
            log += f"\nMessage: {response.text}"
        print(log)


