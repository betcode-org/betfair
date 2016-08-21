import unittest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.racecard import RaceCard
from betfairlightweight.exceptions import APIError


class RaceCardTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.race_card = RaceCard(self.client)

    def test_init(self):
        assert self.race_card.timeout == 3.05
        assert self.race_card._error == APIError
        assert self.race_card.client == self.client
        assert self.race_card.app_key is None

    def test_url(self):
        assert self.race_card.url == 'https://www.betfair.com/rest/v2/raceCard'
        assert self.race_card.login_url == 'https://www.betfair.com/exchange/plus/'

    def test_headers(self):
        assert self.race_card.headers == {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'X-Application': None
        }

    def test_create_req(self):
        assert self.race_card.create_req(['1', '2']) == {
            'dataEntries': ['RACE', 'TIMEFORM_DATA', 'RUNNERS', 'RUNNER_DETAILS'],
            'marketId': '1,2'
        }
        assert self.race_card.create_req(['1', '2'], ['RACE']) == {
            'dataEntries': ['RACE'],
            'marketId': '1,2'
        }

    def test_request(self):
        pass

    def test_login(self):
        pass

    def test_get_race_card(self):
        pass
