import datetime

from .exceptions import StatusCodeError


def check_status_code(response, codes=None):
    """
    Checks response.status_code is in codes.

    :param requests.request response: Requests response
    :param list codes: List of accepted codes or callable
    :raises: StatusCodeError if code invalid
    """
    codes = codes or [200]
    if response.status_code not in codes:
        raise StatusCodeError(response.status_code)


def strp_betfair_time(datetime_string):
    """
    Converts Betfair string to datetime.

    :param str datetime_string: Datetime string.
    """
    try:
        return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except TypeError:
        return None
    except ValueError:
        return None


def strp_betfair_integer_time(datetime_integer):
    """
    Converts Betfair integer to utc datetime.

    :param int datetime_integer: Datetime integer.
    """
    try:
        return datetime.datetime.utcfromtimestamp(datetime_integer / 1e3)
    except TypeError:
        return None


def price_check(data, number):
    """
    Access price data from dictionary.

    :param {} data: Dict object.
    :param int number: Number.
    """
    try:
        output = data[number].price
    except KeyError:
        output = None
    except IndexError:
        output = None
    return output


def size_check(data, number):
    """
    Access size data from dictionary.

    :param {} data: Dict object.
    :param int number: Number.
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


def clean_locals(data):
    """
    Clean up locals dict, remove empty and self/session/params params
    and convert to camelCase.

    :param {} data: locals dicts from a function.
    :returns: dict
    """
    if data.get('params') is not None:
        return data.get('params')
    else:
        return {
            to_camel_case(k): v for k, v in data.items() if v is not None and k not in ['self', 'session', 'params']
        }


def to_camel_case(snake_str):
    """
    Converts snake_string to camelCase

    :param str snake_str:
    :returns: str
    """
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])
