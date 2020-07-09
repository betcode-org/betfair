import time
import requests
from typing import Union

from .baseendpoint import BaseEndpoint
from ..resources import LoginResource
from ..exceptions import LoginError, APIError, InvalidResponse
from ..utils import check_status_code
from ..compat import json


class Login(BaseEndpoint):
    """
    Login operations.
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
        self.client.set_session_token(response_json.get("sessionToken"))
        return self.process_response(
            response_json, LoginResource, elapsed_time, lightweight
        )

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> (dict, float):
        session = session or self.client.session
        time_sent = time.time()
        try:
            response = session.post(
                self.url,
                data=self.data,
                headers=self.client.login_headers,
                cert=self.client.cert,
            )
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
        if response.get("loginStatus") != "SUCCESS":
            raise self._error(response)

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.identity_cert_uri, "certlogin")

    @property
    def data(self) -> dict:
        return {"username": self.client.username, "password": self.client.password}
