import requests

from ..utils import request
from .baseendpoint import BaseEndpoint
from ..compat import json


class Navigation(BaseEndpoint):
    """
    Navigation operations.
    """

    def list_navigation(self, session: requests.Session = None) -> dict:
        """
        This Navigation Data for Applications service allows the retrieval of the
        full Betfair market navigation menu from a compressed file.

        :param requests.session session: Requests session object

        :rtype: json
        """
        return self.request(session=session)

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> dict:
        return request(session=session or self.client.session,
                       method="get",
                       url=self.url,
                       headers=self.client.request_headers,
                       read_timeout=self.read_timeout, connect_timeout=self.connect_timeout)[1]

    @property
    def url(self) -> str:
        return self.client.navigation_uri
