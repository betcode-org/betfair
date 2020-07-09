import time
import requests
from typing import Union

from .baseendpoint import BaseEndpoint
from ..resources import LogoutResource
from ..exceptions import LogoutError, APIError, InvalidResponse
from ..utils import check_status_code
from ..compat import json


class Logout(BaseEndpoint):
    """
    Logout operations.
    """

    _error = LogoutError

    def __call__(
        self, session: requests.Session = None, lightweight: bool = None
    ) -> Union[dict, LogoutResource]:
        """
        Makes logout request.

        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: LogoutResource
        """
        (response, response_json, elapsed_time) = self.request(session=session)
        self.client.client_logout()
        return self.process_response(
            response_json, LogoutResource, elapsed_time, lightweight
        )

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> (dict, float):
        session = session or self.client.session
        time_sent = time.time()
        try:
            response = session.post(self.url, headers=self.client.keep_alive_headers)
        except requests.ConnectionError as e:
            raise APIError(None, exception=e)
        except Exception as e:
            raise APIError(None, exception=e)
        elapsed_time = time.time() - time_sent

        check_status_code(response)
        try:
            response_json = json.loads(response.content.decode("utf-8"))
        except ValueError:
            raise InvalidResponse(response.text)

        if self._error_handler:
            self._error_handler(response_json)
        return response, response_json, elapsed_time

    def _error_handler(
        self, response: dict, method: str = None, params: dict = None
    ) -> None:
        if response.get("status") != "SUCCESS":
            raise self._error(response)

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.identity_uri, "logout")
