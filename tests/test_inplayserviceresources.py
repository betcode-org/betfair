import unittest

from betfairlightweight import resources
from tests.tools import create_mock_json


class InPlayServiceTest(unittest.TestCase):
    def test_scores(self):
        mock_response = create_mock_json("tests/resources/scores.json")
        resource = resources.Scores(**mock_response.json())

        assert isinstance(resource, resources.Scores)
        assert resource.event_type_id == 1

    def test_event_timeline(self):
        mock_response = create_mock_json("tests/resources/eventtimeline.json")
        resource = resources.EventTimeline(**mock_response.json())

        assert isinstance(resource, resources.EventTimeline)
        assert resource.event_type_id == 1

    def test_scores_and_broadcast(self):
        mock_response = create_mock_json("tests/resources/scoresandbroadcast.json")
        resource = resources.ScoresAndBroadcast(**mock_response.json())

        assert isinstance(resource, resources.ScoresAndBroadcast)
        assert isinstance(resource, resources.Scores)
        assert resource.event_type_id == 2
        assert resource.event_id == 33163030
        assert resource.score.home.name == "J Smith"
        assert resource.score.away.name == "R Jones"
        assert len(resource.broadcasts.tv) == 1
        assert resource.broadcasts.tv[0].channel == "Sky Sports Main Event"
        assert resource.broadcasts.tv[0].start_time is not None
        assert resource.broadcasts.tv[0].end_time is not None
        assert resource.broadcasts.radio.url == "http://radio.betfair.com"
        assert (
            resource.broadcasts.bf_live_video.channel
            == "http://livevideo.betfair.com/Default.do?mi=226657935"
        )
        assert resource.broadcasts.is_live_video_available is True
        assert resource.broadcasts.is_data_visualization_available is False
        assert resource.broadcasts.is_paddock_view_available is False
        assert resource.broadcasts.channel == "WEB"
        assert resource.match_info.surface == ""
        assert resource.match_info.number_of_sets == "3"

    def test_scores_and_broadcast_empty(self):
        mock_response = create_mock_json("tests/resources/scores.json")
        resource = resources.ScoresAndBroadcast(**mock_response.json())

        assert isinstance(resource, resources.ScoresAndBroadcast)
        assert resource.event_type_id == 1
        assert resource.broadcasts is None
        assert resource.match_info is None
