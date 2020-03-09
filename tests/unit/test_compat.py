import unittest
import datetime

from betfairlightweight import compat


class CompatTest(unittest.TestCase):
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
