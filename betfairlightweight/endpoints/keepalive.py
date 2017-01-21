import datetime
from requests import ConnectionError

from .baseendpoint import BaseEndpoint
from ..resources import KeepAliveResource
from ..exceptions import KeepAliveError, APIError
from ..utils import check_status_code


class KeepAlive(BaseEndpoint):

    _error = KeepAliveError

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.utcnow()
        response = self.request(session=session)
        response_json = response.json()
        self.client.set_session_token(response_json.get('token'))
        return self.process_response(response_json, KeepAliveResource, date_time_sent)

    def request(self, payload=None, params=None, session=None):
        session = session or self.client.session
        try:
            response = session.post(self.url, headers=self.client.keep_alive_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, exception=e)

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json())
        return response

    def _error_handler(self, response, method=None, params=None):
        if response.get('status') != 'SUCCESS':
            raise self._error(response)

    @property
    def url(self):
        return '%s%s' % (self.client.identity_uri, 'keepAlive')
