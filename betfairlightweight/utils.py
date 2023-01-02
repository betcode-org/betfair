import bz2
import gzip
import io
import os
import re

import requests
import datetime
from typing import Optional, TextIO

from .compat import BETFAIR_DATE_FORMAT
from .exceptions import StatusCodeError
from .__version__ import __title__, __version__

CAMEL_CASE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")
TICK_SIZES = {
    1.0: 0.01,
    2.0: 0.02,
    3.0: 0.05,
    4.0: 0.1,
    6.0: 0.2,
    10.0: 0.5,
    20.0: 1.0,
    30.0: 2.0,
    50.0: 5.0,
    100.0: 10.0,
    1000.0: 1000,
}


def check_status_code(response: requests.Response, codes: list = None) -> None:
    """
    Checks response.status_code is in codes.

    :param requests.request response: Requests response
    :param list codes: List of accepted codes or callable
    :raises: StatusCodeError if code invalid
    """
    codes = codes or [200]
    if response.status_code not in codes:
        raise StatusCodeError(response.status_code)


def clean_locals(data: dict) -> dict:
    """
    Clean up locals dict, remove empty and self/session/params params
    and convert to camelCase.

    :param {} data: locals dicts from a function.
    :returns: dict
    """
    if data.get("params") is not None:
        return data.get("params")
    else:
        return {
            to_camel_case(k): v
            for k, v in data.items()
            if v is not None and k not in ["self", "session", "params", "lightweight"]
        }


def to_camel_case(snake_str: str) -> str:
    """
    Converts snake_string to camelCase

    :param str snake_str:
    :returns: str
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(camel_case_str: str) -> str:
    """
    Utility function for converting a CamelCase formatted string to a snake_case one. The inverse of to_camel_case. Taken from https://stackoverflow.com/a/1176023/2798232

    :param camel_case_str: A string written in CamelCase
    :return: The string rewritten in snake_case
    """
    snake_case_str = CAMEL_CASE_PATTERN.sub("_", camel_case_str).lower()
    return snake_case_str


def default_user_agent():
    return "{0}/{1}".format(__title__, __version__)


def create_date_string(date: datetime.datetime) -> Optional[str]:
    """
    Convert datetime to betfair
    date string.
    """
    if date:
        return date.strftime(BETFAIR_DATE_FORMAT)


def stream_reader(path: str) -> TextIO:
    """Return a text reader for the given path, transparently handling compression inferred by the filename.

    Generally used by methods which read stored streams.
    """
    # this is true when builtins.open is patched, e.g. `with unittest.mock.patch("builtins.open", smart_open.open):`
    if open is not io.open:
        return open(path, "rt")

    _, ext = os.path.splitext(path)
    if ext == ".bz2":
        # as seen in the betfair historical data API
        return bz2.open(path, "rt")
    if ext == ".gz":
        # as seen in example flumine stream recorder
        return gzip.open(path, "rt")
    # as seen in example flumine stream recorder, and unpacked tars from historical data API
    return open(path, "r")
