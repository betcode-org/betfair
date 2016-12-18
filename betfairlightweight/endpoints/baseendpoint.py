import json
from requests import ConnectionError

from ..exceptions import APIError
from ..utils import check_status_code


class BaseEndpoint(object):

    connect_timeout = 3.05
    read_timeout = 16
    _error = APIError

    def __init__(self, parent):
        """
        :param parent: API client.
        """
        self.client = parent

    def request(self, method, params, session):
        """
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request, if None will use MockParams Enum.  # todo
        :param session: Requests session to be used, reduces latency.
        """
        session = session or self.client.session
        request = self.create_req(method, params)
        try:
            response = session.post(self.url, data=request, headers=self.client.request_headers,
                                    timeout=(self.connect_timeout, self.read_timeout))
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json(), method, params)
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

    def _error_handler(self, response, method=None, params=None):
        """
        :param response: Json response.
        :param params: Params to be used in request.
        :param method: Betfair api-ng method to be used.
        :return: None if no error or _error raised.
        """
        if response.get('result'):
            return
        elif response.get('error'):
            raise self._error(response, method, params)

    @staticmethod
    def process_response(response_json, resource, date_time_sent):
        """
        :param response_json: Response in json format
        :param resource: Resource data structure
        :param date_time_sent: Date time sent
        """
        if isinstance(response_json, list):
            return [resource(date_time_sent=date_time_sent, **x) for x in response_json]
        else:
            response_result = response_json.get('result', response_json)
            if isinstance(response_result, list):
                return [resource(date_time_sent=date_time_sent, **x) for x in response_result]
            else:
                return resource(date_time_sent=date_time_sent, **response_result)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'betting/json-rpc/v1')
