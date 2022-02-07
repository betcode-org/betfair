import re
import unittest

from betfairlightweight import __version__


class ReleaseTests(unittest.TestCase):
    @unittest.skipIf("b" in __version__, "test_version: beta version")
    def test_version(self):
        with open("HISTORY.rst", "r") as f:
            version = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", f.read())[0]
        self.assertEqual(__version__, version)
