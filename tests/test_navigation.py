import unittest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.navigation import Navigation
from betfairlightweight.exceptions import APIError


class NavigationInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        navigation = Navigation(client)
        assert navigation.timeout == 3.05
        assert navigation._error == APIError
        assert navigation.client == client


class NavigationTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.navigation = Navigation(client)

    def test_url(self):
        assert self.navigation.client.navigation_uri
