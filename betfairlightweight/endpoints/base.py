import json

from ..exceptions import APIError
from ..utils import check_status_code


class BaseEndpoint:

    timeout = 3.05
    _error = APIError

    def __init__(self, parent):
        """
        :param parent: API client.
        """
        self.client = parent

    def request(self, url, method, params=None, session=None):
        """
        :param url: URL to be used for request.
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request, if None will use MockParams Enum.  # todo
        :param session: Requests session to be used, reduces latency.
        """
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

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json(), params, method)
        return response

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
