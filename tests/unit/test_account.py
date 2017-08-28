import unittest
from tests import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints.account import Account
from betfairlightweight.exceptions import APIError


class AccountInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        account = Account(client)
        assert account.connect_timeout == 6.05
        assert account.read_timeout == 16
        assert account._error == APIError
        assert account.client == client
        assert account.URI == 'AccountAPING/v1.0/'


class AccountTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.account = Account(client)

    def test_init(self):
        assert self.account.URI == 'AccountAPING/v1.0/'
        assert self.account.connect_timeout == 6.05

    @mock.patch('betfairlightweight.endpoints.account.Account.process_response')
    @mock.patch('betfairlightweight.endpoints.account.Account.request', return_value=(mock.Mock(), mock.Mock()))
    def test_get_account_funds(self, mock_request, mock_process_response):
        self.account.get_account_funds()

        mock_request.assert_called_once_with('AccountAPING/v1.0/getAccountFunds', {}, None)
        assert mock_process_response.call_count == 1

    @mock.patch('betfairlightweight.endpoints.account.Account.process_response')
    @mock.patch('betfairlightweight.endpoints.account.Account.request', return_value=(mock.Mock(), mock.Mock()))
    def test_get_account_details(self, mock_request, mock_process_response):
        self.account.get_account_details()

        mock_request.assert_called_once_with('AccountAPING/v1.0/getAccountDetails', {}, None)
        assert mock_process_response.call_count == 1

    @mock.patch('betfairlightweight.endpoints.account.Account.process_response')
    @mock.patch('betfairlightweight.endpoints.account.Account.request', return_value=(mock.Mock(), mock.Mock()))
    def test_get_account_statement(self, mock_request, mock_process_response):
        self.account.get_account_statement()

        mock_request.assert_called_once_with('AccountAPING/v1.0/getAccountStatement', {'itemDateRange': {'from': None, 'to': None}}, None)
        assert mock_process_response.call_count == 1

    @mock.patch('betfairlightweight.endpoints.account.Account.process_response')
    @mock.patch('betfairlightweight.endpoints.account.Account.request', return_value=(mock.Mock(), mock.Mock()))
    def test_list_currency_rates(self, mock_request, mock_process_response):
        self.account.list_currency_rates()

        mock_request.assert_called_once_with('AccountAPING/v1.0/listCurrencyRates', {}, None)
        assert mock_process_response.call_count == 1

    def test_transfer_funds(self):
        with self.assertRaises(DeprecationWarning):
            self.account.transfer_funds()

    def test_url(self):
        assert self.account.url == '%s%s' % (self.account.client.api_uri, 'account/json-rpc/v1')
