from requests import ConnectionError

from ..exceptions import APIError
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint


class Navigation(BaseEndpoint):
    """
    Navigation operations.
    """

    def list_navigation(self, session=None):
        """
        This Navigation Data for Applications service allows the retrieval of the
        full Betfair market navigation menu from a compressed file.

        :param requests.session session: Requests session object

        :rtype: json
        """
        return self.request(session=session)

    def request(self, method=None, params=None, session=None):
        session = session or self.client.session
        try:
            response = session.get(self.url, headers=self.client.request_headers,
                                   timeout=(self.connect_timeout, self.read_timeout))
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        return response.json()

    @property
    def url(self):
        return self.client.navigation_uri
