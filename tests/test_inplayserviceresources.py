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
        mock_response = create_mock_json("tests/resources/scores_and_broadcast.json")
        resource = resources.ScoresAndBroadcast(**mock_response.json())

        assert isinstance(resource, resources.ScoresAndBroadcast)
        assert resource.event_type_id == 1
        assert resource.event_id == 28210051
        assert resource.score is not None
        assert resource.score.home.name == "Boluspor"
        assert resource.score.away.name == "Sanliurfaspor"
        assert resource.full_time_elapsed is not None
        assert resource.status == "SecondHalfKickOff"
        assert resource.match_status == "SecondHalfKickOff"
        assert len(resource.broadcasts) == 1
        assert resource.broadcasts[0].event_id == 28210051
        assert resource.broadcasts[0].has_live_streaming is True
        assert resource.broadcasts[0].has_live_streaming_info is True
        assert resource.broadcasts[0].img_url == "https://example.com/img.png"
        assert resource.broadcasts[0].overview_url == "https://example.com/overview"
        assert resource.broadcasts[0].provider == "PROVIDER"
        assert resource.broadcasts[0].provider_name == "Provider Name"
        assert resource.broadcasts[0].provider_display_name == "Provider Display Name"
        assert resource.broadcasts[0].channels == ["channel1", "channel2"]
        assert resource.match_info is not None
        assert resource.match_info.event_id == 28210051
        assert resource.match_info.match_id == "12345"
        assert resource.match_info.home_team == "Boluspor"
        assert resource.match_info.away_team == "Sanliurfaspor"
        assert resource.match_info.competition == "Turkish League"
        assert resource.match_info.event_type_id == 1
        assert resource.match_info.start_time is not None
        assert resource.match_info.venue == "Stadium"
        assert resource.match_info.in_play is True

    def test_scores_and_broadcast_minimal(self):
        """Test ScoresAndBroadcast with minimal data (no broadcasts/matchInfo)."""
        resource = resources.ScoresAndBroadcast(
            eventId=123,
            eventTypeId=1,
            status="InProgress",
        )

        assert isinstance(resource, resources.ScoresAndBroadcast)
        assert resource.event_id == 123
        assert resource.event_type_id == 1
        assert resource.score is None
        assert resource.full_time_elapsed is None
        assert resource.broadcasts == []
        assert resource.match_info is None
