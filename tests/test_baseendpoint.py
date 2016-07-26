import unittest
import json

from betfairlightweight import APIClient
from betfairlightweight.endpoints.base import BaseEndpoint
from betfairlightweight.exceptions import APIError


class BaseEndpointInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        base_endpoint = BaseEndpoint(client)
        assert base_endpoint.timeout == 3.05
        assert base_endpoint._error == APIError
        assert base_endpoint.exchange == client.exchange


class BaseClientTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.base_endpoint = BaseEndpoint(client)

    def test_base_endpoint_request(self):
        pass

    def test_base_endpoint_create_resp(self):
        pass

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
