import urllib.parse
import requests
import json
from test_framework.config.config import URL
from termcolor import colored


class ApiCall:
    base_url = URL.BASE_URL
    path = ''

    def __init__(self, headers=None, payload=None, query_params=None, debug=False, **kwargs):
        self.id = None
        self._url = urllib.parse.urljoin(self.base_url, self.path)  #TODO use urlparse to parse into pieces and rejoin
        self.headers = headers
        self.payload = payload
        self.query_params = query_params
        self.debug = debug
        self.kwargs = kwargs

    @property
    def url(self):
        # getter
        if self.id:
            return self._url + '/' + str(self.id)
        else:
            return self._url

    @url.setter
    def url(self, url):
        # setter
        self._url = url

    def call(self, method):
        if self.debug:
            self.log_request(method)
        response = requests.request(method, self.url, data=self.payload.json(), headers=self.headers,
                                    params=self.query_params)
        if self.debug:
            self.log_response(response)
        return response

    def post(self):
        return self.call('post')

    def put(self, id_):
        self.id = id_
        return self.call('put')

    def get(self, id_=None):
        if id_:
            self.id = id_
        return self.call('get')

    def delete(self, id_):
        self.id = id_
        return self.call('delete')

    def log_request(self, method):
        log = colored(f"\n---->Request", color='cyan')
        log += f"\n{method.upper()} {self.url}"
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
        log = colored(f"\n<----Response", color='cyan')
        log += f"\nStatus code: {response.status_code if response.ok else colored(response.status_code, color='red')}"
        if response:
            log += f"\nBody: {json.dumps(response.json(), indent=2)}"
        if not response.ok:
            log += f"\nMessage: {response.text}"
        print(log)
