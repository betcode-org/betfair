import unittest
import datetime

from betfairlightweight import compat


class CompatTest(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(compat.BETFAIR_DATE_FORMAT, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(compat.basestring, (str, bytes))
        self.assertEqual(compat.numeric_types, (int, float))
        self.assertEqual(compat.integer_types, (int,))

    def test_json_loads(self):
        self.assertEqual(
            compat.json.loads('{"lastTradedPrice": 1000}'), {"lastTradedPrice": 1000}
        )

    def test_parse_datetime(self):
        self.assertIsNone(compat.parse_datetime(""))
        self.assertEqual(
            compat.parse_datetime("2016-08-17T18:10:00.000Z"),
            datetime.datetime(2016, 8, 17, 18, 10),
        )
        self.assertEqual(
            compat.parse_datetime("2016-08-17T18:10:01.000Z"),
            datetime.datetime(2016, 8, 17, 18, 10, 1),
        )
        self.assertEqual(
            compat.parse_datetime("2016-08-17T18:10:01.321Z"),
            datetime.datetime(2016, 8, 17, 18, 10, 1, 321000),
        )
