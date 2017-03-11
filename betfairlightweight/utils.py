import datetime

from .enums import MockParams
from .exceptions import StatusCodeError


def check_status_code(response, codes=None):
    """Checks response.status_code is in codes

    :param response: Requests response
    :param codes: List of accepted codes or callable
    :raises: StatusCodeError if code invalid
    """
    codes = codes or [200]
    if response.status_code not in codes:
        raise StatusCodeError(response.status_code)


# def api_request(func):
#     """Checks params and provides MockParams if None
#
#     :param func: api request function.
#     """
#     api_request_name = func.__name__
#
#     def _api_request(api, params=None, session=None, exchange=None):
#         if not api.check_session:
#             raise SessionTokenError()
#         if not params:
#             params = MockParams[api_request_name].value
#             return func(api, params, session, exchange)
#         else:
#             return func(api, params, session, exchange)
#     return _api_request


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
    """Converts Betfair integer to utc datetime.

    :param datetime_integer: Datetime integer.
    """
    try:
        return datetime.datetime.utcfromtimestamp(datetime_integer / 1e3)
    except TypeError:
        return None


def price_check(data, number):
    """Access price data from dictionary.

    :param data: Dict object.
    :param number: Number.
    """
    try:
        output = data[number].price
    except KeyError:
        output = None
    except IndexError:
        output = None
    return output


def size_check(data, number):
    """Access size data from dictionary.

    :param data: Dict object.
    :param number: Number.
    """
    try:
        output = data[number].size
    except KeyError:
        output = None
    except IndexError:
        output = None
    return output


def update_available(available, book_update, deletion_select):
    for book in book_update:
        updated = False
        for (count, trade) in enumerate(available):
            if trade[0] == book[0]:
                if book[deletion_select] == 0:
                    del available[count]
                    updated = True
                    break
                else:
                    available[count] = book
                    updated = True
                    break

        if not updated and book[deletion_select] != 0:
            # handles betfair bug, http://forum.bdp.betfair.com/showthread.php?t=3351
            available.append(book)
