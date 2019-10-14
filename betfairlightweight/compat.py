import datetime

basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int,)

# will attempt to use c libraries if installed

try:
    import ujson as json

    def json_loads(s, **kwargs):
        return json.loads(s, precise_float=True, **kwargs)
except ImportError:
    import json

    def json_loads(s, **kwargs):
        return json.loads(s, **kwargs)

try:
    import ciso8601

    def parse_datetime(datetime_string):
        try:
            return ciso8601.parse_datetime_as_naive(datetime_string)
        except ValueError:
            return
except ImportError:
    def parse_datetime(datetime_string):
        try:
            return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return
