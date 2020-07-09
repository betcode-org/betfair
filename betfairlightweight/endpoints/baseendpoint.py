import time
import requests
from typing import Union, Type

from ..baseclient import BaseClient
from ..exceptions import APIError, InvalidResponse
from ..utils import check_status_code
from ..compat import json
from ..resources import BaseResource


class BaseEndpoint:

    connect_timeout = 3.05
    read_timeout = 16
    _error = APIError

    def __init__(self, parent: BaseClient):
        """
        :param parent: API client.
        """
        self.client = parent

    def request(
        self, method: str, params: dict, session: requests.Session
    ) -> (dict, float):
        """
        :param str method: Betfair api-ng method to be used.
        :param dict params: Params to be used in request
        :param Session session: Requests session to be used, reduces latency.
        """
        session = session or self.client.session
        request = self.create_req(method, params)
        time_sent = time.time()
        try:
            response = session.post(
                self.url,
                data=request,
                headers=self.client.request_headers,
                timeout=(self.connect_timeout, self.read_timeout),
            )
        except requests.ConnectionError as e:
            raise APIError(None, method, params, e)
        except Exception as e:
            raise APIError(None, method, params, e)
        elapsed_time = time.time() - time_sent

        check_status_code(response)
        try:
            response_json = json.loads(response.content.decode("utf-8"))
        except ValueError:
            raise InvalidResponse(response.text)

        if self._error_handler:
            self._error_handler(response_json, method, params)
        return response, response_json, elapsed_time

    @staticmethod
    def create_req(method: str, params: dict) -> str:
        """
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request.
        :return: Json payload.
        """
        return json.dumps(
            {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        )

    def _error_handler(
        self, response: dict, method: str = None, params: dict = None
    ) -> None:
        """
        :param response: Json response.
        :param params: Params to be used in request.
        :param method: Betfair api-ng method to be used.
        :return: None if no error or _error raised.
        """
        if response.get("result"):
            return
        elif response.get("error"):
            raise self._error(response, method, params)

    def process_response(
        self,
        response_json: Union[dict, list],
        resource: Type[BaseResource],
        elapsed_time: float,
        lightweight: bool,
    ) -> Union[BaseResource, dict, list]:
        """
        :param requests.Response response: requests Response object
        :param dict/list response_json: Response in dict format
        :param BaseResource resource: Resource data structure
        :param float elapsed_time: Elapsed time of request
        :param bool lightweight: If True will return dict not a resource (22x faster)
        """
        if isinstance(response_json, list):
            result = response_json
        else:
            result = response_json.get("result", response_json)

        if lightweight:
            return result
        elif self.client.lightweight and lightweight is not False:
            return result
        elif isinstance(result, list):
            try:
                return [resource(elapsed_time=elapsed_time, **x) for x in result]
            except TypeError:
                raise InvalidResponse(response=result)
        else:
            try:
                return resource(elapsed_time=elapsed_time, **result)
            except TypeError:
                raise InvalidResponse(response=result)

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.api_uri, "betting/json-rpc/v1")
