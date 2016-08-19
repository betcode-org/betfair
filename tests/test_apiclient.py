import unittest

from betfairlightweight.apiclient import APIClient


class APIClientInit(unittest.TestCase):

    def test_base_client_init(self):
        client = APIClient('username', 'password', 'app_key')
        assert str(client) == 'APIClient'
        assert repr(client) == '<APIClient [username]>'
