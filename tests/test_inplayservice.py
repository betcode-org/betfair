import unittest
from unittest import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints.inplayservice import InPlayService
from betfairlightweight.exceptions import APIError


class InPlayServiceTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.in_play_service = InPlayService(self.client)

    def test_init(self):
        assert self.in_play_service.connect_timeout == 3.05
        assert self.in_play_service.read_timeout == 16
        assert self.in_play_service._error == APIError
        assert self.in_play_service.client == self.client

    @mock.patch('betfairlightweight.endpoints.inplayservice.InPlayService.process_response')
    @mock.patch('betfairlightweight.endpoints.inplayservice.InPlayService.request')
    def test_get_event_timeline(self, mock_request, mock_process_response):
        event_id = [12345]
        params = {
            'eventId': event_id,
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        self.in_play_service.get_event_timeline(event_id)

        mock_request.assert_called_with(
                url='https://www.betfair.com/inplayservice/v1.1/eventTimeline', session=None, params=params)
        assert mock_request.call_count == 1
        assert mock_process_response.call_count == 1

    @mock.patch('betfairlightweight.endpoints.inplayservice.InPlayService.process_response')
    @mock.patch('betfairlightweight.endpoints.inplayservice.InPlayService.request')
    def test_get_scores(self, mock_request, mock_process_response):
        event_ids = [12345]
        params = {
            'eventIds': ','.join(str(x) for x in event_ids),
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        self.in_play_service.get_scores(event_ids)

        mock_request.assert_called_with(
                url='https://www.betfair.com/inplayservice/v1.1/scores', session=None, params=params)
        assert mock_request.call_count == 1
        assert mock_process_response.call_count == 1

    @mock.patch('betfairlightweight.endpoints.inplayservice.check_status_code')
    @mock.patch('betfairlightweight.endpoints.inplayservice.InPlayService.headers')
    def test_request(self, mock_headers, mock_check_status_code):
        mock_session = mock.Mock()
        mock_session.get.return_value = None
        params = [1, 2, 3]
        url = '123'

        self.in_play_service.request(session=mock_session, params=params, url=url)

        mock_session.get.assert_called_with(
                url, headers=mock_headers, params=params)
        assert mock_session.get.call_count == 1

    def test_headers(self):
        assert self.in_play_service.headers == {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        }

    def test_url(self):
        assert self.in_play_service.url == 'https://www.betfair.com/inplayservice/v1.1/'
