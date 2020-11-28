from typing import Optional
from datetime import datetime


BETFAIR_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int,)

# will attempt to use C/Rust libraries if installed

try:
    import orjson as json
except ImportError:
    import json


try:
    import ciso8601

    def parse_datetime(datetime_string: str) -> Optional[datetime]:
        try:
            return ciso8601.parse_datetime_as_naive(datetime_string)
        except ValueError:
            return


except ImportError:

    def parse_datetime(datetime_string: str) -> Optional[datetime]:
        try:
            return datetime.strptime(datetime_string, BETFAIR_DATE_FORMAT)
        except ValueError:
            return
