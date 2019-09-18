import urllib.parse
import requests
import json
from test.config.config import URL


class ApiCall:
    base_url = URL.BASE_URL
    path = ''

    def __init__(self, headers=None, payload=None, query_params=None, debug=False, **kwargs):
        self.id = None
        self._url = self.url  #TODO is this ok ?
        self.headers = headers
        self.payload = payload
        self.query_params = query_params
        self.debug = debug
        self.kwargs = kwargs

    @property
    def url(self):
        url = urllib.parse.urljoin(self.base_url, self.path)
        if self.id:
            url.format(id=self.id)
        return url

    @url.setter
    def url(self, url):
        self._url = url

    def call(self, method):
        if self.debug:
            self.log_request(method)
        response = requests.request(method, self._url, data=self.payload.json(), headers=self.headers,
                                    params=self.query_params)
        if self.debug:
            self.log_response(response)
        return response

    def post(self):
        return self.call('post')

    def put(self, id_):
        self.append_id(id_)
        return self.call('put')

    def get(self, id=None):
        if id:
            self.append_id(id)
        return self.call('get')

    def delete(self, id_):
        self.append_id(id_)
        return self.call('delete')

    def append_id(self, id_):
        self._url = self._url + '/' + str(id_)

    def log_request(self, method):
        log = f"\n---->Request: \n{method.upper()} {self. url}"
        if self.headers:
            log += f"\nheaders = {self.headers}"
        if self.query_params:
            log += f"\nquery_params = {self.query_params}"
        if self.payload:
            log += f"\npayload = {self.payload.json()}"
        if self.kwargs:
            log += f"\n**kwargs = {self.kwargs}"
        print(log)

    @staticmethod
    def log_response(response):
        log = f"\n<----Response: \nStatus code: {response.status_code}"
        if response:
            log += f"\nBody: {json.dumps(response.json(), indent=2)}"
        if not response.ok:
            log += f"\nMessage: {response.text}"
        print(log)
