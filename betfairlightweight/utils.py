from .exceptions import StatusCodeError

TICK_SIZES = {1.0: 0.01, 2.0: 0.02, 3.0: 0.05, 4.0: 0.1, 6.0: 0.2, 10.0: 0.5,
              20.0: 1.0, 30.0: 2.0, 50.0: 5.0, 100.0: 10.0, 1000.0: 1000}


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
            to_camel_case(k): v for k, v in data.items() if v is not None and k not in
            ['self', 'session', 'params', 'lightweight']
        }


def to_camel_case(snake_str):
    """
    Converts snake_string to camelCase

    :param str snake_str:
    :returns: str
    """
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])
