import unittest
from unittest import mock

from betfairlightweight import APIClient
from betfairlightweight import resources
from betfairlightweight.endpoints.scores import Scores
from betfairlightweight.exceptions import APIError
from tests.unit.tools import create_mock_json


class ScoresInit(unittest.TestCase):
    def test_base_endpoint_init(self):
        client = APIClient("username", "password", "app_key")
        scores = Scores(client)
        assert scores.connect_timeout == 3.05
        assert scores._error == APIError
        assert scores.client == client
        assert scores.URI == "ScoresAPING/v1.0/"


class ScoresTest(unittest.TestCase):
    def setUp(self):
        client = APIClient("username", "password", "app_key", "UK")
        self.scores = Scores(client)

    @mock.patch("betfairlightweight.endpoints.scores.Scores.request")
    def test_list_race_details(self, mock_response):
        mock = create_mock_json("tests/resources/list_race_details.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.5)

        response = self.scores.list_race_details()
        assert mock.json.call_count == 1
        mock_response.assert_called_with("ScoresAPING/v1.0/listRaceDetails", {}, None)
        assert isinstance(response[0], resources.RaceDetails)
        assert len(response) == 475

    @mock.patch("betfairlightweight.endpoints.scores.Scores.request")
    def test_list_available_events(self, mock_response):
        mock = create_mock_json("tests/resources/availableevents.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.3)

        response = self.scores.list_available_events()
        assert mock.json.call_count == 1
        mock_response.assert_called_with(
            "ScoresAPING/v1.0/listAvailableEvents", {}, None
        )
        assert all(isinstance(event, resources.AvailableEvent) for event in response)

    @mock.patch("betfairlightweight.endpoints.scores.Scores.request")
    def test_list_scores(self, mock_response):
        mock = create_mock_json("tests/resources/score.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.3)
        mock_update_keys = mock.Mock()

        response = self.scores.list_scores(mock_update_keys)
        assert mock.json.call_count == 1
        mock_response.assert_called_with(
            "ScoresAPING/v1.0/listScores", {"updateKeys": mock_update_keys}, None
        )
        assert all(isinstance(event, resources.Score) for event in response)

    @mock.patch("betfairlightweight.endpoints.scores.Scores.request")
    def test_list_incidents(self, mock_response):
        mock = create_mock_json("tests/resources/incidents.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.3)
        mock_update_keys = mock.Mock()

        response = self.scores.list_incidents(mock_update_keys)
        assert mock.json.call_count == 1
        mock_response.assert_called_with(
            "ScoresAPING/v1.0/listIncidents", {"updateKeys": mock_update_keys}, None
        )
        assert all(isinstance(event, resources.Incidents) for event in response)

    def test_url(self):
        assert self.scores.url == "%s%s" % (
            self.scores.client.api_uri,
            "scores/json-rpc/v1",
        )
