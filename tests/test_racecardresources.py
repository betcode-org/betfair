from __future__ import print_function

import unittest
import datetime

from betfairlightweight import resources

from tests.tools import create_mock_json


class RaceCardResourcesTest(unittest.TestCase):
    DATE_TIME_SENT = datetime.datetime(2003, 8, 4, 12, 30, 45)

    def test_racecard(self):
        mock_response = create_mock_json('tests/resources/racecard.json')
        racecard = mock_response.json().get('result')
        resource = resources.RaceCard(date_time_sent=self.DATE_TIME_SENT,
                                      **racecard)
        assert isinstance(resource, resources.RaceCard)

#
