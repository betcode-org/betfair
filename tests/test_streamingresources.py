import unittest

from betfairlightweight.resources.streamingresources import (
    CricketMatch,
    MarketDefinition,
    MarketDefinitionRunner,
    Race,
    RaceProgress,
    RaceChange,
)
from tests.tools import create_mock_json


class TestMarketDefinition(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json(
            "tests/resources/streaming_market_definition.json"
        )
        self.market_definition = MarketDefinition(**self.mock_response.json())

    def test_init(self):
        assert len(self.market_definition.runners) == 7
        assert self.market_definition.bsp_market is True
        assert self.market_definition.market_base_rate == 5
        assert len(self.market_definition.key_line_definitions.key_line) == 2

    def test_missing_open_date(self):
        response_json = dict(self.mock_response.json())
        response_json.pop("openDate")
        market_definition = MarketDefinition(**response_json)
        assert market_definition.open_date is None

    def test_extra_data(self):
        mock_response = create_mock_json(
            "tests/resources/streaming_market_definition.json"
        )
        mock_response_json = mock_response.json()
        mock_response_json["bando"] = "bill"
        assert MarketDefinition(**mock_response_json)


class TestMarketDefinitionRunner(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json(
            "tests/resources/streaming_market_definition.json"
        )
        market_definition = self.mock_response.json()
        runner = market_definition["runners"][0]
        self.market_definition_runner = MarketDefinitionRunner(**runner)

    def test_init(self):
        assert self.market_definition_runner.selection_id == 11131804
        assert self.market_definition_runner.adjustment_factor == 44.323
        assert self.market_definition_runner.sort_priority == 1
        assert self.market_definition_runner.status == "ACTIVE"
        assert self.market_definition_runner.removal_date is None

    def test_str(self):
        assert str(self.market_definition_runner) == "MarketDefinitionRunner: 11131804"

    def test_repr(self):
        assert repr(self.market_definition_runner) == "<MarketDefinitionRunner>"


class TestRace(unittest.TestCase):
    def setUp(self):
        self.mock_response = {
            "mid": "1.123",
            "id": "1234.56",
            "rpc": {"hi": "world"},
            "rrc": [{"test": "me"}],
        }
        self.race = Race(**self.mock_response)

    def test_init(self):
        assert self.race.market_id == "1.123"
        assert self.race.race_id == "1234.56"
        self.assertIsInstance(self.race.race_progress, RaceProgress)
        self.assertIsInstance(self.race.race_runners[0], RaceChange)


class TestRaceProgress(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/streaming_rcm.json")
        self.race_progress = RaceProgress(**self.mock_response.json()["rc"][0]["rpc"])

    def test_init(self):
        assert self.race_progress.feed_time_epoch == 1518626674
        assert self.race_progress.gate_name == "1f"
        assert self.race_progress.sectional_time == 10.6
        assert self.race_progress.running_time == 46.7
        assert self.race_progress.speed == 17.8
        assert self.race_progress.progress == 87.5
        assert self.race_progress.order == [
            7390417,
            5600338,
            11527189,
            6395118,
            8706072,
        ]
        assert self.race_progress.warn == 0


class TestRaceChange(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/streaming_rcm.json")
        self.race_change = RaceChange(**self.mock_response.json()["rc"][0]["rrc"][0])

    def test_init(self):
        assert self.race_change.feed_time_epoch == 1518626674
        assert self.race_change.selection_id == 7390417
        assert self.race_change.lat == 51.4189543
        assert self.race_change.long == -0.4058491
        assert self.race_change.speed == 17.8
        assert self.race_change.progress == 2051
        assert self.race_change.stride_frequency == 2.07


class TestCricketMatch0(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/ccms/ccm0.json")
        self.cricket_match = CricketMatch(**self.mock_response.json()["cc"][0])

    def test_init(self):
        assert self.cricket_match.event_id == "30610310"
        assert self.cricket_match.market_id == "1.179676557"
        assert self.cricket_match.fixture_info.expected_start_time == 1643295600000
        assert self.cricket_match.fixture_info.fixture_status == "IN_RUNNING"
        assert (
            self.cricket_match.fixture_info.event_description
            == "Karachi Kings v Multan Sultans, Pakistan Super League Match 1, from National Stadium"
        )
        assert self.cricket_match.fixture_info.max_overs == 20
        assert self.cricket_match.fixture_info.event_status == "BALL_IN_PROGRESS"
        assert self.cricket_match.home_team is None
        assert self.cricket_match.away_team is None
        assert self.cricket_match.match_stats.current_innings == 1
        assert self.cricket_match.match_stats.innings_stats[0].innings_num == 1
        assert (
            self.cricket_match.match_stats.innings_stats[0].batting_team
            == "Karachi Kings"
        )
        assert (
            self.cricket_match.match_stats.innings_stats[0].bowling_team
            == "Multan Sultans"
        )
        assert self.cricket_match.match_stats.innings_stats[0].innings_runs == 80
        assert self.cricket_match.match_stats.innings_stats[0].innings_overs == "12.5"
        assert self.cricket_match.match_stats.innings_stats[0].innings_wickets == 2
        assert (
            self.cricket_match.match_stats.batting_team_stats.team_name
            == "Karachi Kings"
        )
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_runs == 4
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_strike == 0
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_runs == 8
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_strike == 1
        assert (
            self.cricket_match.match_stats.bowling_team_stats.team_name
            == "Multan Sultans"
        )
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_wickets is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_wickets is None
        assert self.cricket_match.match_stats.winner == "NA"
        assert (
            self.cricket_match.match_stats.scoreboard_status
            == "Match in Progress - Ball in Progress (est.latency:3 seconds)"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[0].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[0].overs == "12.5"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].actual_time
            == 1643299013861
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[1].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[1].overs == "12.4"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].actual_time
            == 1643298990238
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].incident_type
            == "WIDE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[2].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[2].overs == "12.3"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].actual_time
            == 1643298961522
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].modified is True
        )


class TestCricketMatch1(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/ccms/ccm1.json")
        self.cricket_match = CricketMatch(**self.mock_response.json()["cc"][0])

    def test_init(self):
        assert self.cricket_match.event_id == "30610359"
        assert self.cricket_match.market_id == "1.179676556"
        assert self.cricket_match.fixture_info.expected_start_time == 1643293800000
        assert self.cricket_match.fixture_info.fixture_status == "IN_RUNNING"
        assert (
            self.cricket_match.fixture_info.event_description
            == "World Giants v India Maharajas, Legends Cricket League Match 6, from Al Amerat Cricket Ground Oman Cricket (Ministry Turf 1)"
        )
        assert self.cricket_match.fixture_info.max_overs == 20
        assert self.cricket_match.fixture_info.event_status == "BALL_IN_PROGRESS"
        assert self.cricket_match.home_team is None
        assert self.cricket_match.away_team is None
        assert self.cricket_match.match_stats.current_innings == 1
        assert self.cricket_match.match_stats.innings_stats[0].innings_num == 1
        assert (
            self.cricket_match.match_stats.innings_stats[0].batting_team
            == "World Giants"
        )
        assert (
            self.cricket_match.match_stats.innings_stats[0].bowling_team
            == "India Maharajas"
        )
        assert self.cricket_match.match_stats.innings_stats[0].innings_runs == 186
        assert self.cricket_match.match_stats.innings_stats[0].innings_overs == "15.5"
        assert self.cricket_match.match_stats.innings_stats[0].innings_wickets == 3
        assert (
            self.cricket_match.match_stats.batting_team_stats.team_name
            == "World Giants"
        )
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_runs == 83
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_strike == 0
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_runs == 0
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_strike == 1
        assert (
            self.cricket_match.match_stats.bowling_team_stats.team_name
            == "India Maharajas"
        )
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_wickets is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_wickets is None
        assert self.cricket_match.match_stats.winner == "NA"
        assert (
            self.cricket_match.match_stats.scoreboard_status
            == "Match in Progress - Ball in Progress (est.latency:3 seconds)"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].incident_type
            == "OUT"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].qualifier_type
            is None
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[0].value is None
        assert self.cricket_match.incident_list_wrapper.incident_list[0].overs == "15.5"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].actual_time
            == 1643298137862
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[1].value == "0"
        assert self.cricket_match.incident_list_wrapper.incident_list[1].overs == "15.4"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].actual_time
            == 1643298112170
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[2].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[2].overs == "15.3"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].actual_time
            == 1643298085471
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].modified is False
        )


class TestCricketMatch2(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/ccms/ccm2.json")
        self.cricket_match = CricketMatch(**self.mock_response.json()["cc"][0])

    def test_init(self):
        assert self.cricket_match.event_id == "30610280"
        assert self.cricket_match.market_id == "1.179668557"
        assert self.cricket_match.fixture_info.expected_start_time == 1643359200000
        assert self.cricket_match.fixture_info.fixture_status == "IN_RUNNING"
        assert (
            self.cricket_match.fixture_info.event_description
            == "TRAINING: Perth Scorchers v Sydney Sixers, Big Bash League Final, from Docklands Stadium"
        )
        assert self.cricket_match.fixture_info.max_overs == 20
        assert self.cricket_match.fixture_info.event_status == "MATCH_STABLE"
        assert self.cricket_match.home_team is None
        assert self.cricket_match.away_team is None
        assert self.cricket_match.match_stats.current_innings == 2
        assert self.cricket_match.match_stats.innings_stats[0].innings_num == 2
        assert (
            self.cricket_match.match_stats.innings_stats[0].batting_team
            == "Sydney Sixers"
        )
        assert (
            self.cricket_match.match_stats.innings_stats[0].bowling_team
            == "Perth Scorchers"
        )
        assert self.cricket_match.match_stats.innings_stats[0].innings_runs == 6
        assert self.cricket_match.match_stats.innings_stats[0].innings_overs == "1.4"
        assert self.cricket_match.match_stats.innings_stats[0].innings_wickets == 1
        assert self.cricket_match.match_stats.innings_stats[1].innings_num == 1
        assert (
            self.cricket_match.match_stats.innings_stats[1].batting_team
            == "Perth Scorchers"
        )
        assert (
            self.cricket_match.match_stats.innings_stats[1].bowling_team
            == "Sydney Sixers"
        )
        assert self.cricket_match.match_stats.innings_stats[1].innings_runs == 171
        assert self.cricket_match.match_stats.innings_stats[1].innings_overs == "20"
        assert self.cricket_match.match_stats.innings_stats[1].innings_wickets == 6
        assert (
            self.cricket_match.match_stats.batting_team_stats.team_name
            == "Sydney Sixers"
        )
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_runs == 0
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_strike == 1
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_runs == 3
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_strike == 0
        assert (
            self.cricket_match.match_stats.bowling_team_stats.team_name
            == "Perth Scorchers"
        )
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_wickets is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_wickets is None
        assert self.cricket_match.match_stats.winner == "NA"
        assert (
            self.cricket_match.match_stats.scoreboard_status
            == "Match in Progress - Ball in Progress (est.latency:3 seconds)"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].participant_ref
            == "Daniel Hughes"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[0].value == "0"
        assert self.cricket_match.incident_list_wrapper.incident_list[0].innings == 2
        assert self.cricket_match.incident_list_wrapper.incident_list[0].overs == "1.4"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].actual_time
            == 1643366603847
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].incident_type
            == "OUT"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].qualifier_type
            is None
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[1].value is None
        assert self.cricket_match.incident_list_wrapper.incident_list[1].overs == "1.3"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].actual_time
            == 1643366467184
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[2].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[2].overs == "1.2"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].actual_time
            == 1643366432553
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].modified is False
        )


class TestCricketMatch3(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json("tests/resources/ccms/ccm3.json")
        self.cricket_match = CricketMatch(**self.mock_response.json()["cc"][0])

    def test_init(self):
        assert self.cricket_match.event_id == "30610280"
        assert self.cricket_match.market_id == "1.179668557"
        assert self.cricket_match.fixture_info.expected_start_time == 1643359200000
        assert self.cricket_match.fixture_info.fixture_status == "IN_RUNNING"
        assert (
            self.cricket_match.fixture_info.event_description
            == "TRAINING: Perth Scorchers v Sydney Sixers, Big Bash League Final, from Docklands Stadium"
        )
        assert self.cricket_match.fixture_info.max_overs == 20
        assert self.cricket_match.fixture_info.event_status == "BALL_IN_PROGRESS"
        assert self.cricket_match.home_team is None
        assert self.cricket_match.away_team is None
        assert self.cricket_match.match_stats.current_innings == 1
        assert self.cricket_match.match_stats.innings_stats[0].innings_num == 1
        assert (
            self.cricket_match.match_stats.innings_stats[0].batting_team
            == "Perth Scorchers"
        )
        assert (
            self.cricket_match.match_stats.innings_stats[0].bowling_team
            == "Sydney Sixers"
        )
        assert self.cricket_match.match_stats.innings_stats[0].innings_runs == 169
        assert self.cricket_match.match_stats.innings_stats[0].innings_overs == "19.5"
        assert self.cricket_match.match_stats.innings_stats[0].innings_wickets == 6
        assert (
            self.cricket_match.match_stats.batting_team_stats.team_name
            == "Perth Scorchers"
        )
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_runs == 74
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_1_strike == 1
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_name is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_runs == 1
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_balls is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_fours is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_sixes is None
        assert self.cricket_match.match_stats.batting_team_stats.bat_2_strike == 0
        assert (
            self.cricket_match.match_stats.bowling_team_stats.team_name
            == "Sydney Sixers"
        )
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_1_wickets is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_name is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_overs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_runs is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_maidens is None
        assert self.cricket_match.match_stats.bowling_team_stats.bowl_2_wickets is None
        assert self.cricket_match.match_stats.winner == "NA"
        assert (
            self.cricket_match.match_stats.scoreboard_status
            == "Match in Progress - Ball in Progress (est.latency:3 seconds)"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].incident_type
            == "NO_BALL"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[0].value == "2"
        assert self.cricket_match.incident_list_wrapper.incident_list[0].overs == "19.5"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].actual_time
            == 1643365137339
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[0].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].incident_type
            == "WIDE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[1].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[1].overs == "19.4"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].actual_time
            == 1643365102771
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[1].modified is False
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].participant_ref
            is None
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].incident_type
            == "STRIKE"
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].qualifier_type
            == "RUNS"
        )
        assert self.cricket_match.incident_list_wrapper.incident_list[2].value == "1"
        assert self.cricket_match.incident_list_wrapper.incident_list[2].overs == "19.3"
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].actual_time
            == 1643365029126
        )
        assert (
            self.cricket_match.incident_list_wrapper.incident_list[2].modified is False
        )
