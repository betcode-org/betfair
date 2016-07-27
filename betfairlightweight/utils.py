import datetime

from .parse.enums import MockParams
from .exceptions import SessionTokenError, StatusCodeError


def check_status_code(response, codes=None):
    """Checks response.status_code is in codes

    :param response: Requests response
    :param codes: List of accepted codes or callable
    :raises: StatusCodeError if code invalid
    """
    codes = codes or [200]
    if response.status_code not in codes:
        raise StatusCodeError(response.status_code)


def api_request(func):
    """Checks params and provides MockParams if None

    :param func: api request function.
    """
    api_request_name = func.__name__

    def _api_request(api, params=None, session=None, exchange=None):
        if not api.check_session:
            raise SessionTokenError()
        if not params:
            params = MockParams[api_request_name].value
            return func(api, params, session, exchange)
        else:
            return func(api, params, session, exchange)
    return _api_request


def process_request(request, session, model):
    """Processes response based on response_result

    :param request: __call__ function from apimethod.
    :param session: Requests session, if provided.
    :param model: Model to be used for parsing.
    """
    (response, raw_response, sent) = request(session)
    if isinstance(response, list):
        return [model(sent, raw_response, x) for x in response]
    else:
        response_result = response.get('result')
        if isinstance(response_result, list):
            return [model(sent, raw_response, x) for x in response_result]
        else:
            return model(sent, raw_response, response_result)


def strp_betfair_time(datetime_string):
    """Converts Betfair string to datetime.

    :param datetime_string: Datetime string.
    """
    try:
        return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except TypeError:
        return None
    except ValueError:
        return None


def strp_betfair_integer_time(datetime_integer):
    """Converts Betfair integer to datetime.

    :param datetime_integer: Datetime integer.
    """
    try:
        return datetime.datetime.fromtimestamp(datetime_integer / 1e3)
    except TypeError:
        return None
    except ValueError:
        return None


def price_check(data, number, key):
    """Access data from dictionary.

    :param data: Dict object.
    :param number: Number.
    :param key: Key.
    """
    try:
        output = data[number][key]
    except KeyError:
        output = None
    except IndexError:
        output = None
    return output
