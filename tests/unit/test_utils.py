import unittest
from mock import Mock

from betfairlightweight.utils import (
    check_status_code,
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


class UtilsTestCleanLocals(unittest.TestCase):

    def test_clean_locals(self, params=None, filter=123):
        params = clean_locals(locals())
        assert params == {'filter': 123}

    def test_clean_locals_params(self, params={'test': 456}, filter=123):
        params = clean_locals(locals())
        assert params == {'test': 456}
