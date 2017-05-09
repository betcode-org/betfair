import datetime
from requests import ConnectionError

from .baseendpoint import BaseEndpoint
from ..resources import KeepAliveResource
from ..exceptions import KeepAliveError, APIError
from ..utils import check_status_code


class KeepAlive(BaseEndpoint):
    """
    KeepAlive operations.
    """

    _error = KeepAliveError

    def __call__(self, session=None, lightweight=None):
        """
        Makes keep alive request.

        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: KeepAliveResource
        """
        (response, elapsed_time) = self.request(session=session)
        self.client.set_session_token(response.get('token'))
        return self.process_response(response, KeepAliveResource, elapsed_time, lightweight)

    def request(self, payload=None, params=None, session=None):
        session = session or self.client.session
        date_time_sent = datetime.datetime.utcnow()
        try:
            response = session.post(self.url, headers=self.client.keep_alive_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, exception=e)
        elapsed_time = (datetime.datetime.utcnow() - date_time_sent).total_seconds()

        response_data = response.json()

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response_data)
        return response_data, elapsed_time

    def _error_handler(self, response, method=None, params=None):
        if response.get('status') != 'SUCCESS':
            raise self._error(response)

    @property
    def url(self):
        return '%s%s' % (self.client.identity_uri, 'keepAlive')
