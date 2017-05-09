import unittest
import datetime
from mock import Mock

from betfairlightweight.utils import (
    check_status_code,
    update_available,
    clean_locals,
    to_camel_case,
)
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

    def test_convert_to_camel_case(self):
        assert to_camel_case('hello_world') == 'helloWorld'


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


class UtilsTestCleanLocals(unittest.TestCase):

    def test_clean_locals(self, params=None, filter=123):
        params = clean_locals(locals())
        assert params == {'filter': 123}

    def test_clean_locals_params(self, params={'test': 456}, filter=123):
        params = clean_locals(locals())
        assert params == {'test': 456}
