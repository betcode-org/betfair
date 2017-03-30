import unittest

from betfairlightweight.filters import (
    market_filter,
    time_range,
)


class FilterTest(unittest.TestCase):

    def test_time_range(self):
        response = time_range()
        assert response == {'from': None, 'to': None}

        response = time_range(from_='123', to='456')
        assert response == {'from': '123', 'to': '456'}

    def test_market_filter(self):
        response = market_filter()
        assert response == {}

        response = market_filter(marketIds=['1.123'])
        assert response == {'marketIds': ['1.123']}
