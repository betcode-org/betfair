import datetime

from .base import BaseEndpoint
from ..exceptions import KeepAliveError, APIError


class KeepAlive(BaseEndpoint):

    _error = KeepAliveError
    _endpoints_uk = {
        'KeepAlive': 'https://identitysso.betfair.com/api/keepAlive'
    }

    def __call__(self):
        url = self._endpoints_uk['KeepAlive']
        (response, raw_response, sent) = self.request(url)
        self.client.set_session_token(response.get('token'))
        return response

    def request(self, url, payload=None, params=None, session=None):
        if not session:
            session = self.client.session
        date_time_sent = datetime.datetime.now()
        try:
            response = session.post(url, headers=self.client.keep_alive_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, params, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, params, exception=e)
        return self.create_resp(response, date_time_sent)

    def _error_handler(self, response, params=None, method=None):
        if response.get('status') != 'SUCCESS':
            raise self._error(response)
