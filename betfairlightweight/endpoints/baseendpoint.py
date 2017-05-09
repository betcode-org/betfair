import requests
import datetime
import ujson as json
from requests import ConnectionError

from ..exceptions import APIError
from ..utils import check_status_code

# monkeypatching requests
# https://github.com/kennethreitz/requests/issues/1595
requests.models.json = json


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
        :param str method: Betfair api-ng method to be used.
        :param dict params: Params to be used in request
        :param Session session: Requests session to be used, reduces latency.
        """
        session = session or self.client.session
        request = self.create_req(method, params)
        date_time_sent = datetime.datetime.utcnow()
        try:
            response = session.post(
                self.url,
                data=request,
                headers=self.client.request_headers,
                timeout=(self.connect_timeout, self.read_timeout)
            )
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)
        elapsed_time = (datetime.datetime.utcnow()-date_time_sent).total_seconds()

        response_data = response.json()

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response_data, method, params)
        return response_data, elapsed_time

    @staticmethod
    def create_req(method, params):
        """
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request.
        :return: Json payload.
        """
        return json.dumps(
            {
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': 1
            }
        )

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

    def process_response(self, response_json, resource, elapsed_time, lightweight):
        """
        :param dict/list response_json: Response in dict format
        :param BaseResource resource: Resource data structure
        :param float elapsed_time: Elapsed time of request
        :param bool lightweight: If True will return dict not a resource (22x faster)
        """
        if isinstance(response_json, list):
            result = response_json
        else:
            result = response_json.get('result', response_json)

        if lightweight:
            return result
        elif self.client.lightweight and lightweight is not False:
            return result
        elif isinstance(result, list):
            return [resource(elapsed_time=elapsed_time, **x) for x in result]
        else:
            return resource(elapsed_time=elapsed_time, **result)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'betting/json-rpc/v1')
