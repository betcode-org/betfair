
from .base import BaseEndpoint
from ..exceptions import KeepAliveError, APIError
from ..utils import check_status_code


class KeepAlive(BaseEndpoint):

    _error = KeepAliveError

    def __call__(self):
        url = '%s%s' % (self.client.identity_uri, 'keepAlive')
        response = self.request(url)

        response_json = response.json()
        self.client.set_session_token(response_json.get('token'))
        return response_json

    def request(self, url, payload=None, params=None, session=None):
        if not session:
            session = self.client.session
        try:
            response = session.post(url, headers=self.client.keep_alive_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, params, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, params, exception=e)

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json(), params)
        return response

    def _error_handler(self, response, params=None, method=None):
        if response.get('status') != 'SUCCESS':
            raise self._error(response)
