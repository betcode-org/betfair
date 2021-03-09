import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight.compat import json
from betfairlightweight import APIClient
from betfairlightweight.endpoints.historic import Historic
from betfairlightweight.exceptions import APIError


class HistoricalTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("username", "password", "app_key", "UK")
        self.historic = Historic(self.client)

    def test_init(self):
        assert self.historic.client == self.client

    @mock.patch(
        "betfairlightweight.endpoints.historic.Historic.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_my_data(self, mock_request):
        self.historic.get_my_data()

        mock_request.assert_called_with("GetMyData", {}, None)
        assert mock_request.call_count == 1

    @mock.patch(
        "betfairlightweight.endpoints.historic.Historic.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_collection_options(self, mock_request):
        params = {
            "sport": 1,
            "plan": 2,
            "fromDay": 3,
            "fromMonth": 4,
            "fromYear": 5,
            "toDay": 6,
            "toMonth": 7,
            "toYear": 8,
        }
        self.historic.get_collection_options(1, 2, 3, 4, 5, 6, 7, 8)

        mock_request.assert_called_with("GetCollectionOptions", params, None)
        assert mock_request.call_count == 1

    @mock.patch(
        "betfairlightweight.endpoints.historic.Historic.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_data_size(self, mock_request):
        params = {
            "sport": 1,
            "plan": 2,
            "fromDay": 3,
            "fromMonth": 4,
            "fromYear": 5,
            "toDay": 6,
            "toMonth": 7,
            "toYear": 8,
        }
        self.historic.get_data_size(1, 2, 3, 4, 5, 6, 7, 8)

        mock_request.assert_called_with("GetAdvBasketDataSize", params, None)
        assert mock_request.call_count == 1

    @mock.patch(
        "betfairlightweight.endpoints.historic.Historic.request",
        return_value=(mock.Mock(), mock.Mock(), 1.3),
    )
    def test_get_file_list(self, mock_request):
        params = {
            "sport": 1,
            "plan": 2,
            "fromDay": 3,
            "fromMonth": 4,
            "fromYear": 5,
            "toDay": 6,
            "toMonth": 7,
            "toYear": 8,
        }
        self.historic.get_file_list(1, 2, 3, 4, 5, 6, 7, 8)

        mock_request.assert_called_with("DownloadListOfFiles", params, None)
        assert mock_request.call_count == 1

    # def test_download_file(self):
    #     pass

    @mock.patch("betfairlightweight.endpoints.historic.check_status_code")
    @mock.patch("betfairlightweight.endpoints.historic.Historic.headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request(self, mock_post, mock_headers, mock_check_status_code):
        params = {"test": "me"}
        method = "test"
        url = "https://historicdata.betfair.com/api/test"

        mock_response = mock.Mock()
        mock_response.content = "{}".encode("utf-8")
        mock_post.return_value = mock_response

        self.historic.request(method=method, params=params, session=None)

        mock_post.assert_called_with(
            url,
            headers=mock_headers,
            data=json.dumps(params),
            timeout=(self.historic.connect_timeout, self.historic.read_timeout),
        )
        assert mock_post.call_count == 1
        assert mock_check_status_code.call_count == 1

    @mock.patch("betfairlightweight.endpoints.historic.Historic.headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_error(self, mock_post, mock_headers):
        params = {"test": "me"}
        method = "test"
        mock_post.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.historic.request(params=params, method=method, session=None)

        mock_post.side_effect = ValueError()
        with self.assertRaises(APIError):
            self.historic.request(params=params, method=method, session=None)

    # @mock.patch('betfairlightweight.endpoints.historical.check_status_code')
    # @mock.patch('betfairlightweight.endpoints.historical.Historical.headers')
    # @mock.patch('betfairlightweight.baseclient.requests.post')
    # def test_request_json_error(self, mock_post, mock_headers, mock_check_status_code):
    #     params = {'test': 'me'}
    #     method = 'test'
    #     url = 'https://historicdata.betfair.com/api/test'
    #
    #     response = mock.Mock()
    #     mock_post.return_value = response
    #     response.json.side_effect = ValueError()
    #
    #     with self.assertRaises(InvalidResponse):
    #         self.historical.request(params=params, method=method, session=None)

    def test_headers(self):
        assert self.historic.headers == {
            "ssoid": self.client.session_token,
            "Content-Type": "application/json",
        }

    def test_url(self):
        assert self.historic.url == "https://historicdata.betfair.com/api/"
