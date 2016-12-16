import unittest
from tests import mock

from tests.tools import create_mock_json
from betfairlightweight import APIClient
from betfairlightweight.endpoints.betting import Betting
from betfairlightweight.exceptions import APIError
from betfairlightweight import resources


class BettingInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        betting = Betting(client)
        assert betting.connect_timeout == 3.05
        assert betting.read_timeout == 16
        assert betting._error == APIError
        assert betting.client == client
        assert betting.URI == 'SportsAPING/v1.0/'


class BettingTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.betting = Betting(client)

    # def test_set_next_hour(self):
    #     self.betting.set_next_hour()
    #     now = datetime.datetime.now()
    #     assert self.betting._next_hour == (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    #
    # def test_get_transaction_count(self):
    #     params = {'instructions': [1, 2, 3]}
    #     length = self.betting.get_transaction_count(params)
    #     assert length == 3
    #
    #     params = {}
    #     length = self.betting.get_transaction_count(params)
    #     assert length == 0
    #
    # def test_check_transaction_count(self):
    #     params = {'instructions': [1, 2, 3]}
    #     self.betting.check_transaction_count(params)
    #     assert self.betting.transaction_count == 3
    #
    #     now = datetime.datetime.now()
    #     self.betting._next_hour = (now + datetime.timedelta(hours=-1)).replace(minute=0, second=0, microsecond=0)
    #     params = {'instructions': [1, 2, 3]}
    #     self.betting.check_transaction_count(params)
    #     assert self.betting.transaction_count == 3
    #
    #     self.betting.transaction_limit = 2
    #     with self.assertRaises(TransactionCountError):
    #         self.betting.check_transaction_count(params)
    #     assert self.betting.transaction_count == 6

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_event_types(self, mock_response):
        mock = create_mock_json('tests/resources/list_event_types.json')
        mock_response.return_value = mock

        response = self.betting.list_event_types()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listEventTypes', None, None)
        assert isinstance(response[0], resources.EventTypeResult)
        assert len(response) == 2

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_competitions(self, mock_response):
        mock = create_mock_json('tests/resources/list_competitions.json')
        mock_response.return_value = mock

        response = self.betting.list_competitions()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCompetitions', None, None)
        assert isinstance(response[0], resources.CompetitionResult)
        assert len(response) == 22

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_time_ranges(self, mock_response):
        mock = create_mock_json('tests/resources/list_time_ranges.json')
        mock_response.return_value = mock

        response = self.betting.list_time_ranges()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listTimeRanges', None, None)
        assert isinstance(response[0], resources.TimeRangeResult)
        assert len(response) == 30

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_events(self, mock_response):
        mock = create_mock_json('tests/resources/list_events.json')
        mock_response.return_value = mock

        response = self.betting.list_events()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listEvents', None, None)
        assert isinstance(response[0], resources.EventResult)
        assert len(response) == 7

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_types(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_types.json')
        mock_response.return_value = mock

        response = self.betting.list_market_types()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketTypes', None, None)
        assert isinstance(response[0], resources.MarketTypeResult)
        assert len(response) == 25

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_countries(self, mock_response):
        mock = create_mock_json('tests/resources/list_countries.json')
        mock_response.return_value = mock

        response = self.betting.list_countries()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCountries', None, None)
        assert isinstance(response[0], resources.CountryResult)
        assert len(response) == 4

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_venues(self, mock_response):
        mock = create_mock_json('tests/resources/list_venues.json')
        mock_response.return_value = mock

        response = self.betting.list_venues()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listVenues', None, None)
        assert isinstance(response[0], resources.VenueResult)
        assert len(response) == 30

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_catalogue(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_catalogue.json')
        mock_response.return_value = mock

        response = self.betting.list_market_catalogue()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketCatalogue', None, None)
        assert isinstance(response[0], resources.MarketCatalogue)
        assert len(response) == 1

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_book(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_book.json')
        mock_response.return_value = mock

        response = self.betting.list_market_book()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketBook', None, None)
        assert isinstance(response[0], resources.MarketBook)
        assert len(response) == 1

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_current_orders(self, mock_response):
        mock = create_mock_json('tests/resources/list_current_orders.json')
        mock_response.return_value = mock

        response = self.betting.list_current_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCurrentOrders', None, None)
        assert isinstance(response, resources.CurrentOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_cleared_orders(self, mock_response):
        mock = create_mock_json('tests/resources/list_cleared_orders.json')
        mock_response.return_value = mock

        response = self.betting.list_cleared_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listClearedOrders', None, None)
        assert isinstance(response, resources.ClearedOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_place_orders(self, mock_response):
        mock = create_mock_json('tests/resources/place_orders.json')
        mock_response.return_value = mock

        response = self.betting.place_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/placeOrders', None, None)
        assert isinstance(response, resources.PlaceOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_cancel_orders(self, mock_response):
        mock = create_mock_json('tests/resources/cancel_orders.json')
        mock_response.return_value = mock

        response = self.betting.cancel_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/cancelOrders', None, None)
        assert isinstance(response, resources.CancelOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_update_orders(self, mock_response):
        mock = create_mock_json('tests/resources/update_orders.json')
        mock_response.return_value = mock

        response = self.betting.update_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/updateOrders', None, None)
        assert isinstance(response, resources.UpdateOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_replace_orders(self, mock_response):
        mock = create_mock_json('tests/resources/replace_orders.json')
        mock_response.return_value = mock

        response = self.betting.replace_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/replaceOrders', None, None)
        assert isinstance(response, resources.ReplaceOrders)
