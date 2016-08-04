import unittest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.account import Account
from betfairlightweight.exceptions import APIError


class AccountInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        account = Account(client)
        assert account.timeout == 6.05
        assert account._error == APIError
        assert account.client == client
        assert account.URI == 'AccountAPING/v1.0/'


class AccountTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.betting = Account(client)

    def test_url(self):
        assert self.betting.url == '%s%s' % (self.betting.client.api_uri, 'account/json-rpc/v1')
