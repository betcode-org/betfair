import requests

from ..exceptions import APIError, InvalidResponse
from ..utils import check_status_code
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
    ) -> (dict, float):
        session = session or self.client.session
        try:
            response = session.get(
                self.url,
                headers=self.client.request_headers,
                timeout=(self.connect_timeout, self.read_timeout),
            )
        except requests.ConnectionError as e:
            raise APIError(None, method, params, e)
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        try:
            response_json = json.loads(response.content.decode("utf-8"))
        except ValueError:
            raise InvalidResponse(response.text)

        return response_json

    @property
    def url(self) -> str:
        return self.client.navigation_uri
