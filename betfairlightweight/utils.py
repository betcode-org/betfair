import datetime


def key_check(data, key):
    try:
        return data[key]
    except KeyError:
        return None


def strp_betfair_time(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def key_check_datetime(data, key):
    try:
        output = data[key]
        return strp_betfair_time(output)
    except KeyError:
        return None
