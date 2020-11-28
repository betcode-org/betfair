import unittest
import datetime
from unittest import mock

from betfairlightweight import utils
from betfairlightweight.exceptions import StatusCodeError


class UtilsTest(unittest.TestCase):
    def test_check_status_code_ok(self):
        resp = mock.Mock()
        resp.status_code = 200
        assert utils.check_status_code(resp) is None

    def test_check_status_code_fail(self):
        resp = mock.Mock()
        resp.status_code = 400
        with self.assertRaises(StatusCodeError):
            utils.check_status_code(resp)

    def test_clean_locals(self, params=None, filter=123):
        params = utils.clean_locals(locals())
        assert params == {"filter": 123}

    def test_clean_locals_params(self, params={"test": 456}, filter=123):
        params = utils.clean_locals(locals())
        assert params == {"test": 456}

    def test_convert_to_camel_case(self):
        assert utils.to_camel_case("hello_world") == "helloWorld"
        assert utils.to_camel_case("async_") == "async"

    def test_default_user_agent(self):
        assert utils.default_user_agent()

    def test_create_date_string(self):
        self.assertIsNone(utils.create_date_string(None))
        self.assertEqual(
            utils.create_date_string(datetime.datetime(2020, 11, 27)),
            "2020-11-27T00:00:00.000000Z",
        )
