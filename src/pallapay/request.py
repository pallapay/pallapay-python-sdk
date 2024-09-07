import hashlib
import hmac
from datetime import datetime

import requests
from pallapay.utils import error_handler


class RequestsApi:
    __headers: dict

    def __init__(self, api_key: str, secret_key: str, base_url: str, **kwargs):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.base_url = base_url
        self.session = requests.Session()
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    @error_handler
    def set_header(self, header_name, header_value):
        return self.__headers.update({header_name: header_value})

    @error_handler
    def get(self, path, **kwargs):
        self.__set_auth_headers(path, 'GET')
        return self.session.get(self.base_url + path, headers=self.__headers, **kwargs)

    @error_handler
    def post(self, path, **kwargs):
        self.__set_auth_headers(path, 'POST')
        return self.session.post(self.base_url + path, headers=self.__headers, **kwargs)

    @error_handler
    def put(self, path, **kwargs):
        self.__set_auth_headers(path, 'PUT')
        return self.session.put(self.base_url + path, headers=self.__headers, **kwargs)

    @error_handler
    def patch(self, path, **kwargs):
        self.__set_auth_headers(path, 'PATCH')
        return self.session.patch(self.base_url + path, headers=self.__headers, **kwargs)

    @error_handler
    def delete(self, path, **kwargs):
        self.__set_auth_headers(path, 'DELETE')
        return self.session.delete(self.base_url + path, headers=self.__headers, **kwargs)

    def __set_auth_headers(self, path: str, request_method: str):
        timestamp = str(round(datetime.now().timestamp()))
        prepared_str = request_method.upper() + path + timestamp
        signature = hmac.new(
            bytes(self.__secret_key, 'latin-1'),
            msg=bytes(prepared_str, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().lower()

        self.set_header('X-Palla-Api-Key', self.__api_key),
        self.set_header('X-Palla-Timestamp', timestamp),
        self.set_header('X-Palla-Sign', signature),

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsApi.__deep_merge(value, node)
            else:
                destination[key] = value
        return destination
