import unittest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.scores import Scores
from betfairlightweight.exceptions import APIError


class ScoresInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        scores = Scores(client)
        assert scores.timeout == 3.05
        assert scores._error == APIError
        assert scores.client == client
        assert scores.URI == 'ScoresAPING/v1.0/'


class ScoresTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.scores = Scores(client)

    def test_url(self):
        assert '%s%s' % (self.scores.client.api_uri, 'scores/json-rpc/v1')
