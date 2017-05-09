from __future__ import print_function

import unittest
import datetime

from betfairlightweight import resources

from tests.tools import create_mock_json


class ScoreResourcesTest(unittest.TestCase):

    def test_racedetails(self):
        mock_response = create_mock_json('tests/resources/racedetails.json')
        resource = resources.RaceDetails(**mock_response.json())

        assert isinstance(resource, resources.RaceDetails)

    # def test_score(self):
    #     mock_response = create_mock_json('tests/resources/score.json')
    #     resource = resources.Score(**mock_response.json())
    #
    #     assert isinstance(resource, resources.Score)
    #
    # def test_incidents(self):
    #     mock_response = create_mock_json('tests/resources/incidents.json')
    #     resource = resources.Incidents(**mock_response.json())
    #
    #     assert isinstance(resource, resources.Incidents)
    #
    # def test_available_events(self):
    #     mock_response = create_mock_json('tests/resources/availableevents.json')
    #     resource = resources.AvailableEvent(**mock_response.json())
    #
    #     assert isinstance(resource, resources.AvailableEvent)
