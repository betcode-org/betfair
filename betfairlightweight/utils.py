import datetime
from bisect import bisect_right

from .enums import MockParams
from .exceptions import StatusCodeError

TICK_SIZES = {1.0: 0.01, 2.0: 0.02, 3.0: 0.05, 4.0: 0.1, 6.0: 0.2, 10.0: 0.5,
              20.0: 1.0, 30.0: 2.0, 50.0: 5.0, 100.0: 10.0, 1000.0: 1000}


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

        if not updated:
            available.append(book)

def get_price_increment(price):
    '''
    Get the tick size given a reference price.

    :param price: reference price.
    :type price: float
    :returns: Tick size increment.
    :rtype: float
    '''
    price_list = sorted(TICK_SIZES.keys())
    closest_price = price_list[bisect_right(price_list, price)-1]
    return TICK_SIZES.get(closest_price)


def get_bf_prices():
    '''
    Get all tradeable prices for betfair.

    :returns: list of all prices tradeable on betfair.
    :rtype: list
    '''
    level = 1.01
    bet_levels = []
    while level <= 1000.0:
        bet_levels.append(float(str(level)))
        if level < 1.995:
            level += 0.01
        elif level < 2.99:
            level += 0.02
        elif level < 3.99:
            level += 0.05
        elif level < 5.99:
            level += 0.1
        elif level < 9.99:
            level += 0.2
        elif level < 19.99:
            level += 0.5
        elif level < 29.99:
            level += 1.0
        elif level < 49.99:
            level += 2.0
        elif level < 99.99:
            level += 5.0
        elif level < 1001.0:
            level += 10.0
    return bet_levels


def create_timerange(start, end):
    """
    Create an isoformat date range for betfair filtering.

    :param start: start of time range.
    :type start: datetime.datetime
    :param end: end of time range.
    :type end: datetime.datetime
    :returns: isoformat date range.
    :rtype: dict
    """
    try:
        return {'from': start.isoformat(), 'to': end.isoformat()}
    except:
        raise ValueError('Failed to create isoformat dates.')


def clean_locals(data):
    """
    Clean up locals dict, remove empty and self params.

    :param data: locals dicts from a function.
    :type data: dict
    :returns: dict

    """
    return dict((k, v) for k, v in data.iteritems() if v is not None and k != 'self' and k != 'session')

