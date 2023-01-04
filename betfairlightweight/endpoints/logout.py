import requests
from typing import Union, Tuple

from .baseendpoint import BaseEndpoint
from ..resources import LogoutResource
from ..exceptions import LogoutError
from ..utils import request


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
    ) -> Tuple[requests.Response, dict, float]:
        response, data, duration = request(
            session=session or self.client.session,
            method="post",
            url=self.url,
            headers=self.client.keep_alive_headers,
            connect_timeout=self.connect_timeout,
            read_timeout=self.read_timeout)
        if self._error_handler:
            self._error_handler(data)
        return response, data, duration

    def _error_handler(
        self, response: dict, method: str = None, params: dict = None
    ) -> None:
        if response.get("status") != "SUCCESS":
            raise self._error(response)

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.identity_uri, "logout")
