import datetime
import os
import unittest

from betfairlightweight import resources
from tests.unit.tools import create_mock_json


class RaceCardResourcesTest(unittest.TestCase):
    DATE_TIME_SENT = datetime.datetime(2003, 8, 4, 12, 30, 45)

    def test_racecard(self):
        rootdir = "tests/resources/racecards"
        racecards = []
        for _, _, filenames in os.walk(rootdir):
            for json_racecard in [
                fname for fname in filenames if fname.startswith("racecards")
            ]:
                mock_response = create_mock_json(os.path.join(rootdir, json_racecard))
                racecard = mock_response.json().get("result")
                racecards.append(
                    resources.RaceCard(date_time_sent=self.DATE_TIME_SENT, **racecard)
                )
        assert 0 < len(racecards)
        assert all(isinstance(racecard, resources.RaceCard) for racecard in racecards)
