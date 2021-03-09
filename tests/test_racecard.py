import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.racecard import RaceCard
from betfairlightweight.exceptions import APIError, RaceCardError, InvalidResponse


class RaceCardTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("username", "password", "app_key", "UK")
        self.race_card = RaceCard(self.client)

    def test_init(self):
        assert self.race_card.connect_timeout == 3.05
        assert self.race_card._error == APIError
        assert self.race_card.client == self.client
        assert self.race_card.app_key is None

    def test_login(self):
        mock_session = mock.Mock()
        mock_response = mock.Mock()
        mock_response.content = '"appKey": "1234",'.encode("utf-8")
        mock_session.get.return_value = mock_response
        self.race_card.login(mock_session)

        assert self.race_card.app_key == "1234"
        mock_session.get.assert_called_with(self.race_card.login_url)
        assert mock_session.get.call_count == 1

    def test_login_error(self):
        mock_session = mock.Mock()
        mock_response = mock.Mock()
        mock_response.content = '"applesKey": "1234",'.encode("utf-8")
        mock_session.get.return_value = mock_response

        with self.assertRaises(RaceCardError):
            self.race_card.login(mock_session)

        assert self.race_card.app_key is None
        mock_session.get.assert_called_with(self.race_card.login_url)
        assert mock_session.get.call_count == 1

    def test_login_connection_error(self):
        mock_session = mock.Mock()
        mock_session.get.side_effect = ConnectionError()

        with self.assertRaises(APIError):
            self.race_card.login(mock_session)

    def test_login_unknown_error(self):
        mock_session = mock.Mock()
        mock_session.get.side_effect = ValueError()

        with self.assertRaises(APIError):
            self.race_card.login(mock_session)

    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.process_response")
    @mock.patch(
        "betfairlightweight.endpoints.racecard.RaceCard.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_race_card(self, mock_request, mock_process_response):
        market_ids = ["1", "2"]
        data_entries = "test"
        with self.assertRaises(RaceCardError):
            self.race_card.get_race_card(market_ids)

        self.race_card.app_key = "1234"
        self.race_card.get_race_card(market_ids=market_ids, data_entries=data_entries)

        mock_request.assert_called_once_with(
            "raceCard", session=None, params={"marketId": "1,2", "dataEntries": "test"}
        )
        assert mock_request.call_count == 1

    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.process_response")
    @mock.patch(
        "betfairlightweight.endpoints.racecard.RaceCard.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_race_result(self, mock_request, mock_process_response):
        market_ids = ["1", "2"]
        data_entries = "test"
        with self.assertRaises(RaceCardError):
            self.race_card.get_race_result(market_ids)

        self.race_card.app_key = "1234"
        self.race_card.get_race_result(market_ids=market_ids, data_entries=data_entries)

        mock_request.assert_called_once_with(
            "raceResults",
            session=None,
            params={"marketId": "1,2", "sortBy": "DATE_DESC", "dataEntries": "test"},
        )
        assert mock_request.call_count == 1

    @mock.patch("betfairlightweight.endpoints.racecard.check_status_code")
    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.create_req")
    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request(
        self, mock_get, mock_login_headers, mock_create_req, mock_check_status_code
    ):
        mock_login_headers.return_value = {}
        _url = "https://www.betfair.com/rest/v2/test"
        mock_response = mock.Mock()
        mock_response.content = "{}".encode("utf-8")
        mock_get.return_value = mock_response
        self.race_card.request(method="test")

        mock_get.assert_called_with(_url, headers=mock_login_headers, params=None)
        assert mock_get.call_count == 1

    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.create_req")
    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request_error(self, mock_get, mock_login_headers, mock_create_req):
        mock_get.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.race_card.request()

        mock_get.side_effect = ValueError()
        with self.assertRaises(APIError):
            self.race_card.request()

    @mock.patch(
        "betfairlightweight.endpoints.racecard.json.loads", side_effect=ValueError
    )
    @mock.patch("betfairlightweight.endpoints.racecard.check_status_code")
    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.create_req")
    @mock.patch("betfairlightweight.endpoints.racecard.RaceCard.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request_error_invalid_response(
        self,
        mock_get,
        mock_login_headers,
        mock_create_req,
        mock_check_status_code,
        mock_json_loads,
    ):
        response = mock.Mock()
        mock_get.return_value = response

        with self.assertRaises(InvalidResponse):
            self.race_card.request()

    def test_create_race_card_req(self):
        assert self.race_card.create_race_card_req(["1", "2"], None) == {
            "dataEntries": "RACE, TIMEFORM_DATA, RUNNERS, RUNNER_DETAILS",
            "marketId": "1,2",
        }
        assert self.race_card.create_race_card_req(["1", "2"], ["RACE"]) == {
            "dataEntries": ["RACE"],
            "marketId": "1,2",
        }

    def test_create_race_result_req(self):
        assert self.race_card.create_race_result_req(["1", "2"], None) == {
            "dataEntries": "RUNNERS, MARKETS, PRICES, RACE, COURSE",
            "marketId": "1,2",
            "sortBy": "DATE_DESC",
        }
        assert self.race_card.create_race_result_req(["1", "2"], ["RACE"]) == {
            "dataEntries": ["RACE"],
            "marketId": "1,2",
            "sortBy": "DATE_DESC",
        }

    def test_headers(self):
        assert self.race_card.headers == {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-Application": None,
        }

    def test_urls(self):
        assert self.race_card.url == "https://www.betfair.com/rest/v2/"
        assert self.race_card.login_url == "https://www.betfair.com/exchange/plus/"
