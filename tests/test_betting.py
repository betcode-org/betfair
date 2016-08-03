import unittest
import datetime

from betfairlightweight import APIClient
from betfairlightweight.endpoints.betting import Betting
from betfairlightweight.exceptions import APIError, TransactionCountError


class BettingInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        betting = Betting(client)
        assert betting.timeout == 3.05
        assert betting._error == APIError
        assert betting.client == client
        now = datetime.datetime.now()
        assert betting._next_hour == (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        assert betting.transaction_count == 0
        assert betting.transaction_limit == 999
        assert betting.URI == 'SportsAPING/v1.0/'


class BettingTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.betting = Betting(client)

    def test_set_next_hour(self):
        self.betting.set_next_hour()
        now = datetime.datetime.now()
        assert self.betting._next_hour == (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    def test_get_transaction_count(self):
        params = {'instructions': [1, 2, 3]}
        length = self.betting.get_transaction_count(params)
        assert length == 3

        params = {}
        length = self.betting.get_transaction_count(params)
        assert length is None

    def test_check_transaction_count(self):
        params = {'instructions': [1, 2, 3]}
        self.betting.check_transaction_count(params)
        assert self.betting.transaction_count == 3

        self.betting.transaction_limit = 2
        with self.assertRaises(TransactionCountError):
            self.betting.check_transaction_count(params)
        assert self.betting.transaction_count == 6
