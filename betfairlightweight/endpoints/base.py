import datetime
import json

from ..errors.apiexceptions import APIError


class BaseEndpoint:

    timeout = 3.05
    _error = APIError
    _endpoints_uk = {}
    _endpoints_aus = {}

    def __init__(self, parent):
        self.client = parent
        self.exchange = parent.exchange

    def request(self, url, method, params=None):
        date_time_sent = datetime.datetime.now()
        session = self.client.request
        request = self.create_req(method, params)
        try:
            response = session.post(url, data=request, headers=self.client.request_headers,
                                    timeout=(self.timeout, 12))
        except ConnectionError:
            raise APIError(None, params, method, 'ConnectionError')
        except Exception as e:
            raise APIError(None, params, method, e)
        return self.create_resp(response, method, params, date_time_sent)

    def create_resp(self, response, date_time_sent, method=None, params=None):
        if response.status_code == 200:
            if self._error_handler:
                self._error_handler(response.json(), params, method)
            return response.json(), response, date_time_sent
        else:
            raise self._error(response, params, method)

    @staticmethod
    def create_req(method, params):
        payload = {'jsonrpc': '2.0',
                   'method': method,
                   'params': params,
                   'id': 1}
        return json.dumps(payload)

    def _error_handler(self, response, params=None, method=None):
        if response.get('result'):
            return
        elif response.get('error'):
            raise self._error(response, params, method)
