import datetime
from requests import ConnectionError

from .baseendpoint import BaseEndpoint
from ..resources import LogoutResource
from ..exceptions import LogoutError, APIError
from ..utils import check_status_code


class Logout(BaseEndpoint):
    """
    Logout operations.
    """

    _error = LogoutError

    def __call__(self, session=None, lightweight=None):
        """
        Makes logout request.

        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: LogoutResource
        """
        (response, elapsed_time) = self.request(session=session)
        self.client.client_logout()
        return self.process_response(response, LogoutResource, elapsed_time, lightweight)

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
        return '%s%s' % (self.client.identity_uri, 'logout')
