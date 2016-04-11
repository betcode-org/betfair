import datetime


def strp_betfair_time(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def key_check_datetime(data, key):
    try:
        output = data[key]
        return strp_betfair_time(output)
    except KeyError:
        return None


def price_check(data, number, key):
    try:
        output = data[number][key]
    except KeyError:
        output = None
    except IndexError:
        output = None
    return output


def transaction_count(func, *args, **kwargs):
    self = args[0]
    if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
        self._api_client.check_transaction_count(self.instructions_length)
    return func(*args, **kwargs)
