import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight.compat import json
from betfairlightweight import APIClient
from betfairlightweight.endpoints.baseendpoint import BaseEndpoint
from betfairlightweight.exceptions import APIError, InvalidResponse
from tests.unit.tools import create_mock_json


class BaseEndpointInit(unittest.TestCase):
    def test_base_endpoint_init(self):
        client = APIClient("username", "password", "app_key")
        base_endpoint = BaseEndpoint(client)
        assert base_endpoint.connect_timeout == 3.05
        assert base_endpoint.read_timeout == 16
        assert base_endpoint._error == APIError
        assert base_endpoint.client == client


class BaseEndPointTest(unittest.TestCase):
    def setUp(self):
        client = APIClient("username", "password", "app_key", "UK")
        self.base_endpoint = BaseEndpoint(client)

    def test_base_endpoint_create_req(self):
        payload = {"jsonrpc": "2.0", "method": "test", "params": "empty", "id": 1}
        assert self.base_endpoint.create_req("test", "empty") == json.dumps(payload)

    @mock.patch("betfairlightweight.endpoints.baseendpoint.BaseEndpoint.create_req")
    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.request_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request(self, mock_post, mock_request_headers, mock_cert, mock_create_req):
        mock_response = create_mock_json("tests/resources/login_success.json")
        mock_post.return_value = mock_response

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        response = self.base_endpoint.request(None, None, None)

        mock_post.assert_called_once_with(
            url,
            data=mock_create_req(),
            headers=mock_request_headers,
            timeout=(3.05, 16),
        )
        assert response[1] == mock_response.json()
        assert isinstance(response[2], float)

    @mock.patch("betfairlightweight.endpoints.baseendpoint.BaseEndpoint.create_req")
    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.request_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_error(
        self, mock_post, mock_request_headers, mock_cert, mock_create_req
    ):
        mock_post.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.base_endpoint.request(None, None, None)

        mock_post.side_effect = ValueError()
        with self.assertRaises(APIError):
            self.base_endpoint.request(None, None, None)

    @mock.patch(
        "betfairlightweight.endpoints.baseendpoint.json.loads", side_effect=ValueError
    )
    @mock.patch("betfairlightweight.endpoints.baseendpoint.BaseEndpoint.create_req")
    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.request_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_json_error(
        self,
        mock_post,
        mock_request_headers,
        mock_cert,
        mock_create_req,
        mock_json_loads,
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidResponse):
            self.base_endpoint.request(None, None, None)

    def test_base_endpoint_error_handler(self):
        mock_response = create_mock_json("tests/resources/base_endpoint_success.json")
        assert self.base_endpoint._error_handler(mock_response.json()) is None

        mock_response = create_mock_json("tests/resources/base_endpoint_fail.json")
        with self.assertRaises(APIError):
            self.base_endpoint._error_handler(mock_response.json())

    def test_base_endpoint_process_response(self):
        mock_resource = mock.Mock()

        response_list = [{}, {}]
        response = self.base_endpoint.process_response(
            response_list, mock_resource, None, False
        )
        assert type(response) == list
        assert response[0] == mock_resource()

        response_result_list = {"result": [{}, {}]}
        response = self.base_endpoint.process_response(
            response_result_list, mock_resource, None, False
        )
        assert type(response) == list
        assert response[0] == mock_resource()

        response_result = {"result": {}}
        response = self.base_endpoint.process_response(
            response_result, mock_resource, None, False
        )
        assert response == mock_resource()

        # lightweight tests
        response_list = [{}, {}]
        response = self.base_endpoint.process_response(
            response_list, mock_resource, None, True
        )
        assert response == response_list

        client = APIClient("username", "password", "app_key", lightweight=True)
        base_endpoint = BaseEndpoint(client)
        response_list = [{}, {}]
        response = base_endpoint.process_response(
            response_list, mock_resource, None, False
        )
        assert type(response) == list
        assert response[0] == mock_resource()

    def test_base_endpoint_process_response_no_error(self):
        class MockResource:
            def __init__(self, elapsed_time, hello, **kwargs):
                self.elapsed_time = elapsed_time
                self.hello = hello

        mock_resource = MockResource
        response_list = [{"hello": "world"}]

        response = self.base_endpoint.process_response(
            response_list, mock_resource, 0, False
        )
        assert type(response) == list
        assert (
            response[0].__dict__
            == mock_resource(elapsed_time=0, **response_list[0]).__dict__
        )

    def test_base_endpoint_process_response_error(self):
        class MockResource:
            def __init__(self, elapsed_time, hello):
                self.elapsed_time = elapsed_time
                self.hello = hello

        mock_resource = MockResource
        response_list = [{}]  # missing 'hello'

        with self.assertRaises(InvalidResponse):
            self.base_endpoint.process_response(response_list, mock_resource, 0, False)

    def test_base_endpoint_url(self):
        assert self.base_endpoint.url == "%s%s" % (
            self.base_endpoint.client.api_uri,
            "betting/json-rpc/v1",
        )
