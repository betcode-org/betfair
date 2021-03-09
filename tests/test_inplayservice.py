import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.inplayservice import InPlayService
from betfairlightweight.exceptions import APIError, InvalidResponse


class InPlayServiceTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("username", "password", "app_key", "UK")
        self.in_play_service = InPlayService(self.client)

    def test_init(self):
        assert self.in_play_service.connect_timeout == 3.05
        assert self.in_play_service.read_timeout == 16
        assert self.in_play_service._error == APIError
        assert self.in_play_service.client == self.client

    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.process_response"
    )
    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_event_timeline(self, mock_request, mock_process_response):
        event_id = 12345
        params = {
            "eventId": event_id,
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        self.in_play_service.get_event_timeline(event_id)

        mock_request.assert_called_with(
            url="https://ips.betfair.com/inplayservice/v1.1/eventTimeline",
            session=None,
            params=params,
        )
        assert mock_request.call_count == 1
        assert mock_process_response.call_count == 1

    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.process_response"
    )
    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_event_timelines(self, mock_request, mock_process_response):
        event_ids = [12345, 54321]
        params = {
            "eventIds": "12345,54321",
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        self.in_play_service.get_event_timelines(event_ids)

        mock_request.assert_called_with(
            url="https://ips.betfair.com/inplayservice/v1.1/eventTimelines",
            session=None,
            params=params,
        )
        assert mock_request.call_count == 1
        assert mock_process_response.call_count == 1

    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.process_response"
    )
    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.InPlayService.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_scores(self, mock_request, mock_process_response):
        event_ids = [12345]
        params = {
            "eventIds": ",".join(str(x) for x in event_ids),
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        self.in_play_service.get_scores(event_ids)

        mock_request.assert_called_with(
            url="https://ips.betfair.com/inplayservice/v1.1/scores",
            session=None,
            params=params,
        )
        assert mock_request.call_count == 1
        assert mock_process_response.call_count == 1

    @mock.patch("betfairlightweight.endpoints.inplayservice.check_status_code")
    @mock.patch("betfairlightweight.endpoints.inplayservice.InPlayService.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request(self, mock_get, mock_headers, mock_check_status_code):
        params = [1, 2, 3]
        url = "123"
        mock_response = mock.Mock()
        mock_response.content = "{}".encode("utf-8")
        mock_get.return_value = mock_response

        self.in_play_service.request(params=params, url=url)

        mock_get.assert_called_with(url, headers=mock_headers, params=params)
        assert mock_get.call_count == 1
        assert mock_check_status_code.call_count == 1

    @mock.patch("betfairlightweight.endpoints.inplayservice.InPlayService.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request_error(self, mock_get, mock_headers):
        params = [1, 2, 3]
        url = "123"
        mock_get.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.in_play_service.request(params=params, url=url)

        mock_get.side_effect = ValueError()
        with self.assertRaises(APIError):
            self.in_play_service.request(params=params, url=url)

    @mock.patch(
        "betfairlightweight.endpoints.inplayservice.json.loads", side_effect=ValueError
    )
    @mock.patch("betfairlightweight.endpoints.inplayservice.check_status_code")
    @mock.patch("betfairlightweight.endpoints.inplayservice.InPlayService.headers")
    @mock.patch("betfairlightweight.baseclient.requests.get")
    def test_request_json_error(
        self, mock_get, mock_headers, mock_check_status_code, mock_json_loads
    ):
        params = [1, 2, 3]
        url = "123"

        mock_response = mock.Mock()
        mock_response.text = "{}"
        mock_get.return_value = mock_response

        with self.assertRaises(InvalidResponse):
            self.in_play_service.request(params=params, url=url)

    def test_headers(self):
        assert self.in_play_service.headers == {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }

    def test_url(self):
        assert self.in_play_service.url == "https://ips.betfair.com/inplayservice/v1.1/"
