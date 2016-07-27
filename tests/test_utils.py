import unittest
import datetime
from mock import Mock

from betfairlightweight.utils import check_status_code, strp_betfair_integer_time, strp_betfair_time, price_check
from betfairlightweight.exceptions import StatusCodeError


class UtilsTest(unittest.TestCase):

    def test_check_status_code_ok(self):
        resp = Mock()
        resp.status_code = 200

        assert check_status_code(resp) is None

    def test_check_status_code_fail(self):
        resp = Mock()
        resp.status_code = 400

        with self.assertRaises(StatusCodeError):
            check_status_code(resp)

    def test_api_request(self):
        pass

    def test_process_request(self):
        pass

    def test_strp_betfair_time(self):
        for string in ['2100-06-01T10:10:00.000Z', '2100-06-01T10:10:00.00Z', '2100-06-01T10:10:00.0Z']:
            stripped = strp_betfair_time(string)
            assert type(stripped) == datetime.datetime

        stripped = strp_betfair_time(None)
        assert not stripped

        stripped = strp_betfair_time('45')
        assert not stripped

    def test_strp_betfair_integer_time(self):
        integer = 1465631675000
        stripped = strp_betfair_integer_time(integer)
        assert type(stripped) == datetime.datetime

        stripped = strp_betfair_integer_time(None)
        assert not stripped

        stripped = strp_betfair_integer_time('45')
        assert not stripped

    def test_price_check(self):
        data = [{'price': 12, 'size': 13},
                {'price': 2, 'size': 3}]

        back_a = price_check(data, 0, 'price')
        assert back_a == 12

        back_b = price_check(data, 1, 'price')
        assert back_b == 2

        back_c = price_check(data, 2, 'price')
        assert not back_c

        data = []
        back_a = price_check(data, 0, 'price')
        assert not back_a
