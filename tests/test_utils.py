import unittest
import datetime
from mock import Mock

from betfairlightweight.utils import (
    check_status_code,
    strp_betfair_integer_time,
    strp_betfair_time,
    price_check,
    size_check,
    update_available
)
from betfairlightweight.exceptions import StatusCodeError
from betfairlightweight.resources.bettingresources import PriceSize


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
        data = [PriceSize(**{'price': 12, 'size': 13}),
                PriceSize(**{'price': 2, 'size': 3})]

        back_a = price_check(data, 0)
        assert back_a == 12

        back_b = price_check(data, 1)
        assert back_b == 2

        back_c = price_check(data, 2)
        assert not back_c

        back_d = price_check(data, 5)
        assert not back_d

        data = []
        back_e = price_check(data, 0)
        assert not back_e

    def test_size_check(self):
        data = [PriceSize(**{'price': 12, 'size': 13}),
                PriceSize(**{'price': 2, 'size': 3})]

        back_a = size_check(data, 0)
        assert back_a == 13

        back_b = size_check(data, 1)
        assert back_b == 3

        back_c = size_check(data, 2)
        assert not back_c

        back_d = size_check(data, 5)
        assert not back_d

        data = []
        back_e = size_check(data, 0)
        assert not back_e



class UtilsTestUpdateAvailable(unittest.TestCase):

    # update_available()

    def test_update_available_new_update(self):
        # [price, size]
        book_update = [[30, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[27, 0.95], [13, 28.01], [1.02, 1157.21], [30, 6.9]]

        update_available(current, book_update, 1)
        assert current == expected

        book_update = [[30, 6.9], [1.01, 12]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[27, 0.95], [13, 28.01], [1.02, 1157.21], [30, 6.9], [1.01, 12]]

        update_available(current, book_update, 1)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = []
        expected = [[0, 36, 0.57]]

        update_available(current, book_update, 2)
        assert current == expected

    def test_update_available_new_replace(self):
        # [price, size]
        book_update = [[27, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[27, 6.9], [13, 28.01], [1.02, 1157.21]]

        update_available(current, book_update, 1)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = [[0, 36, 0.57], [1, 38, 3.57]]

        update_available(current, book_update, 2)
        assert current == expected

        # tests handling of betfair bug, http://forum.bdp.betfair.com/showthread.php?t=3351
        book_update = [[2, 0, 0], [1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        current = [[1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        expected = [[1, 1.01, 9835.74], [0, 1.02, 1126.22]]

        update_available(current, book_update, 2)
        assert current == expected

    def test_update_available_new_remove(self):
        book_update = [[27, 0]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[13, 28.01], [1.02, 1157.21]]

        update_available(current, book_update, 1)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0], [1, 38, 0], [0, 38, 3.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = [[0, 38, 3.57]]

        update_available(current, book_update, 2)
        assert current == expected
