import datetime
import json

from ..exceptions import APIError


class BaseEndpoint:

    timeout = 3.05
    _error = APIError
    _endpoints_uk = {}
    _endpoints_aus = {}

    def __init__(self, parent):
        """
        :param parent: API client.
        """
        self.client = parent
        self.exchange = parent.exchange

    def request(self, url, method, params=None, session=None):
        """
        :param url: URL to be used for request.
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request, if None will use MockParams Enum.  # todo
        :param session: Requests session to be used, reduces latency.
        """
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self.client.session
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
        """
        :param response: Raw requests response.
        :param date_time_sent: Datetime request was sent.
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request.
        :return: json response, raw_response and datetime sent.
        """
        if response.status_code == 200:
            if self._error_handler:
                self._error_handler(response.json(), params, method)
            return response.json(), response, date_time_sent
        else:
            raise self._error(response, params, method)

    @staticmethod
    def create_req(method, params):
        """
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request.
        :return: Json payload.
        """
        payload = {'jsonrpc': '2.0',
                   'method': method,
                   'params': params,
                   'id': 1}
        return json.dumps(payload)

    def _error_handler(self, response, params=None, method=None):
        """
        :param response: Json response.
        :param params: Params to be used in request.
        :param method: Betfair api-ng method to be used.
        :return: None if no error or _error raised.
        """
        if response.get('result'):
            return
        elif response.get('error'):
            raise self._error(response, params, method)
