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

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_event_types(self, mock_response):
        mock = create_mock_json('tests/resources/list_event_types.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_event_types()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listEventTypes', {'filter': {}}, None)
        assert isinstance(response[0], resources.EventTypeResult)
        assert len(response) == 2

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_competitions(self, mock_response):
        mock = create_mock_json('tests/resources/list_competitions.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_competitions()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCompetitions', {'filter': {}}, None)
        assert isinstance(response[0], resources.CompetitionResult)
        assert len(response) == 22

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_time_ranges(self, mock_response):
        mock = create_mock_json('tests/resources/list_time_ranges.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_time_ranges()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listTimeRanges', {'granularity': 'DAYS', 'filter': {}}, None)
        assert isinstance(response[0], resources.TimeRangeResult)
        assert len(response) == 30

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_events(self, mock_response):
        mock = create_mock_json('tests/resources/list_events.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_events()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listEvents', {'filter': {}}, None)
        assert isinstance(response[0], resources.EventResult)
        assert len(response) == 7

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_types(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_types.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_market_types()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketTypes', {'filter': {}}, None)
        assert isinstance(response[0], resources.MarketTypeResult)
        assert len(response) == 25

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_countries(self, mock_response):
        mock = create_mock_json('tests/resources/list_countries.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_countries()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCountries', {'filter': {}}, None)
        assert isinstance(response[0], resources.CountryResult)
        assert len(response) == 4

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_venues(self, mock_response):
        mock = create_mock_json('tests/resources/list_venues.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_venues()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listVenues', {'filter': {}}, None)
        assert isinstance(response[0], resources.VenueResult)
        assert len(response) == 30

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_catalogue(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_catalogue.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_market_catalogue()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketCatalogue', {'maxResults': 1, 'filter': {}}, None)
        assert isinstance(response[0], resources.MarketCatalogue)
        assert len(response) == 1

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_market_book(self, mock_response):
        mock = create_mock_json('tests/resources/list_market_book.json')
        mock_response.return_value = (mock.json(), 1.3)
        marketIds = mock.Mock()

        response = self.betting.list_market_book(marketIds)
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listMarketBook', {'marketIds': marketIds}, None)
        assert isinstance(response[0], resources.MarketBook)
        assert len(response) == 1

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_current_orders(self, mock_response):
        mock = create_mock_json('tests/resources/list_current_orders.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_current_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listCurrentOrders', {'dateRange': {'from': None, 'to': None}}, None)
        assert isinstance(response, resources.CurrentOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_list_cleared_orders(self, mock_response):
        mock = create_mock_json('tests/resources/list_cleared_orders.json')
        mock_response.return_value = (mock.json(), 1.3)

        response = self.betting.list_cleared_orders()
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/listClearedOrders', {'settledDateRange': {'to': None, 'from': None}, 'betStatus': 'SETTLED'}, None)
        assert isinstance(response, resources.ClearedOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_place_orders(self, mock_response):
        mock = create_mock_json('tests/resources/place_orders.json')
        mock_response.return_value = (mock.json(), 1.3)
        marketId = mock.Mock()
        instructions = mock.Mock()

        response = self.betting.place_orders(marketId, instructions)
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/placeOrders',
                                         {'marketId': marketId, 'instructions': instructions}, None)
        assert isinstance(response, resources.PlaceOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_cancel_orders(self, mock_response):
        mock = create_mock_json('tests/resources/cancel_orders.json')
        mock_response.return_value = (mock.json(), 1.3)
        marketId = mock.Mock()
        instructions = mock.Mock()

        response = self.betting.cancel_orders(marketId, instructions)
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/cancelOrders',
                                         {'marketId': marketId, 'instructions': instructions}, None)
        assert isinstance(response, resources.CancelOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_update_orders(self, mock_response):
        mock = create_mock_json('tests/resources/update_orders.json')
        mock_response.return_value = (mock.json(), 1.3)
        marketId = mock.Mock()
        instructions = mock.Mock()

        response = self.betting.update_orders(marketId, instructions)
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/updateOrders',
                                         {'marketId': marketId, 'instructions': instructions}, None)
        assert isinstance(response, resources.UpdateOrders)

    @mock.patch('betfairlightweight.endpoints.betting.Betting.request')
    def test_replace_orders(self, mock_response):
        mock = create_mock_json('tests/resources/replace_orders.json')
        mock_response.return_value = (mock.json(), 1.3)
        marketId = mock.Mock()
        instructions = mock.Mock()

        response = self.betting.replace_orders(marketId, instructions)
        assert mock.json.call_count == 1
        mock_response.assert_called_with('SportsAPING/v1.0/replaceOrders',
                                         {'marketId': marketId, 'instructions': instructions}, None)
        assert isinstance(response, resources.ReplaceOrders)
