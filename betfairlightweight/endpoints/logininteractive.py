import requests
from typing import Union, Tuple

from .baseendpoint import BaseEndpoint
from ..resources import LoginResource
from ..exceptions import LoginError
from ..utils import request


class LoginInteractive(BaseEndpoint):
    """
    Interactive Login operations (no certs).
    """

    _error = LoginError

    def __call__(
        self, session: requests.Session = None, lightweight: bool = None
    ) -> Union[dict, LoginResource]:
        """
        Makes login request.

        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: LoginResource
        """
        (response, response_json, elapsed_time) = self.request(
            self.url, session=session
        )
        self.client.set_session_token(response_json.get("token"))
        return self.process_response(
            response_json, LoginResource, elapsed_time, lightweight
        )

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> Tuple[requests.Response, dict, float]:
        response, data, duration = request(
            session=session or self.client.session,
            method="post",
            url=self.url,
            data=self.data,
            headers=self.client.login_headers,
            connect_timeout=self.connect_timeout,
            read_timeout=self.read_timeout,
        )
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
        return "%s%s" % (self.client.identity_uri, "login")

    @property
    def data(self) -> dict:
        return {"username": self.client.username, "password": self.client.password}
