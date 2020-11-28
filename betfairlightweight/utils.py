import requests
import datetime
from typing import Optional

from .compat import BETFAIR_DATE_FORMAT
from .exceptions import StatusCodeError
from .__version__ import __title__, __version__

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


def default_user_agent():
    return "{0}/{1}".format(__title__, __version__)


def create_date_string(date: datetime.datetime) -> Optional[str]:
    """
    Convert datetime to betfair
    date string.
    """
    if date:
        return date.strftime(BETFAIR_DATE_FORMAT)
