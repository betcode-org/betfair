import unittest
from tests import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.racecard import RaceCard
from betfairlightweight.exceptions import APIError, RaceCardError


class RaceCardTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.race_card = RaceCard(self.client)

    def test_init(self):
        assert self.race_card.connect_timeout == 3.05
        assert self.race_card._error == APIError
        assert self.race_card.client == self.client
        assert self.race_card.app_key is None

    def test_login(self):
        mock_session = mock.Mock()
        mock_response = mock.Mock()
        mock_response.text = '"appKey": "1234",'
        mock_session.get.return_value = mock_response
        self.race_card.login(mock_session)

        assert self.race_card.app_key == '1234'
        mock_session.get.assert_called_with(self.race_card.login_url)
        assert mock_session.get.call_count == 1

    def test_login_error(self):
        mock_session = mock.Mock()
        mock_response = mock.Mock()
        mock_response.text = '"applesKey": "1234",'
        mock_session.get.return_value = mock_response

        with self.assertRaises(RaceCardError):
            self.race_card.login(mock_session)

        assert self.race_card.app_key is None
        mock_session.get.assert_called_with(self.race_card.login_url)
        assert mock_session.get.call_count == 1

    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.process_response')
    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.request', return_value=(mock.Mock(), 1.3))
    def test_get_race_card(self, mock_request, mock_process_response):
        market_ids = ['1', '2']
        data_entries = 'test'
        with self.assertRaises(RaceCardError):
            self.race_card.get_race_card(market_ids)

        self.race_card.app_key = '1234'
        self.race_card.get_race_card(market_ids=market_ids, data_entries=data_entries)

        mock_request.assert_called_once_with(session=None, params={'marketId': '1,2', 'dataEntries': 'test'})
        assert mock_request.call_count == 1

    @mock.patch('betfairlightweight.endpoints.racecard.check_status_code')
    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.create_req')
    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.headers')
    @mock.patch('betfairlightweight.baseclient.requests.get')
    def test_request(self, mock_get, mock_login_headers, mock_create_req, mock_check_status_code):
        mock_login_headers.return_value = {}

        self.race_card.request()

        mock_get.assert_called_with(
                self.race_card.url, headers=mock_login_headers, params=None)
        assert mock_get.call_count == 1

    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.create_req')
    @mock.patch('betfairlightweight.endpoints.racecard.RaceCard.headers')
    @mock.patch('betfairlightweight.baseclient.requests.get')
    def test_request_error(self, mock_get, mock_login_headers, mock_create_req):
        mock_get.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.race_card.request()

        mock_get.side_effect = ValueError()
        with self.assertRaises(APIError):
            self.race_card.request()

    def test_create_req(self):
        assert self.race_card.create_race_card_req(['1', '2'], None) == {
            'dataEntries': "RACE, TIMEFORM_DATA, RUNNERS, RUNNER_DETAILS",
            'marketId': '1,2'
        }
        assert self.race_card.create_race_card_req(['1', '2'], ['RACE']) == {
            'dataEntries': ['RACE'],
            'marketId': '1,2'
        }

    def test_headers(self):
        assert self.race_card.headers == {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'X-Application': None
        }

    def test_urls(self):
        assert self.race_card.url == 'https://www.betfair.com/rest/v2/raceCard'
        assert self.race_card.login_url == 'https://www.betfair.com/exchange/plus/'
