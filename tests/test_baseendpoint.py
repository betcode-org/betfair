import unittest
import json
import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints.base import BaseEndpoint
from betfairlightweight.exceptions import APIError


class BaseEndpointInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        base_endpoint = BaseEndpoint(client)
        assert base_endpoint.timeout == 3.05
        assert base_endpoint._error == APIError
        assert base_endpoint.client == client


class BaseEndPointTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.base_endpoint = BaseEndpoint(client)

    @mock.patch('betfairlightweight.baseclient.BaseClient.request_headers')
    @mock.patch('betfairlightweight.endpoints.base.BaseEndpoint.create_req')
    @mock.patch('betfairlightweight.apiclient.requests.post')
    def test_base_endpoint_request(self, mock_post, mock_create_req, mock_request_headers):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        expected_dict = {'hello': 'world'}
        mock_response.json.return_value = expected_dict
        mock_post.return_value = mock_response

        mock_req = mock.Mock()
        mock_req.return_value = {}
        mock_create_req.return_value = mock_req

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_request_headers.return_value = mock_headers

        url = 'http://api.empty.co.uk'
        method = 'justatest'
        response = self.base_endpoint.request(url, method)

        mock_post.assert_called_once_with(url, data=mock_req,
                                          headers=mock_request_headers,
                                          timeout=(3.05, 12))
        assert response == mock_response

    def test_base_endpoint_create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': 'test',
                   'params': 'empty',
                   'id': 1}
        assert self.base_endpoint.create_req('test', 'empty') == json.dumps(payload)

    def test_base_endpoint_error_handler(self):
        response = {'result': 'empty'}
        assert self.base_endpoint._error_handler(response) is None

        response = {'error': {'code': -32700}}
        with self.assertRaises(APIError):
            self.base_endpoint._error_handler(response)
