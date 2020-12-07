import unittest

from betfairlightweight.resources.streamingresources import (
    MarketDefinition,
    MarketDefinitionRunner,
    Race,
    RaceProgress,
    RaceChange,
)
from tests.unit.tools import create_mock_json


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
