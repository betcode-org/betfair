import datetime

from betfairlightweight.utils import strp_betfair_time, price_check, strp_betfair_integer_time


def test_api_request():
    pass


def test_process_request():
    pass


def test_strp_betfair_time():
    for string in ['2100-06-01T10:10:00.000Z', '2100-06-01T10:10:00.00Z', '2100-06-01T10:10:00.0Z']:
        stripped = strp_betfair_time(string)
        assert type(stripped) == datetime.datetime

    stripped = strp_betfair_time(None)
    assert not stripped

    stripped = strp_betfair_time('45')
    assert not stripped


def test_strp_betfair_integer_time():
    integer = 1465631675000
    stripped = strp_betfair_integer_time(integer)
    assert type(stripped) == datetime.datetime

    stripped = strp_betfair_integer_time(None)
    assert not stripped

    stripped = strp_betfair_integer_time('45')
    assert not stripped


def test_price_check():
    data = [{'price': 12, 'size': 13},
            {'price': 2, 'size': 3}]

    back_a = price_check(data, 0, 'price')
    assert back_a == 12

    back_b = price_check(data, 1, 'price')
    assert back_b == 2

    back_c = price_check(data, 2, 'price')
    assert not back_c

    data = []
    back_a = price_check(data, 0, 'price')
    assert not back_a
