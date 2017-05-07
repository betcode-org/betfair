from __future__ import print_function

import unittest
import datetime

from betfairlightweight import resources

from tests.tools import create_mock_json


class InPlayServiceTest(unittest.TestCase):

    def test_scores(self):
        mock_response = create_mock_json('tests/resources/scores.json')
        resource = resources.Scores(**mock_response.json())

        assert isinstance(resource, resources.Scores)
        assert resource.event_type_id == 1

    def test_event_timeline(self):
        mock_response = create_mock_json('tests/resources/eventtimeline.json')
        resource = resources.EventTimeline(**mock_response.json())

        assert isinstance(resource, resources.EventTimeline)
        assert resource.event_type_id == 1
