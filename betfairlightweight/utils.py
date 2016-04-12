import datetime
from .parse.enums import MockParams
from .errors.apiexceptions import ParameterError


def process_response(response, raw_response, sent, model):
    response_result = response.get('result')
    if isinstance(response_result, list):
        return [model(sent, raw_response, x) for x in response_result]
    else:
        return model(sent, raw_response, response_result)


def api_request(func, *args, **kwargs):
    api_request_name = func.__name__

    def api_request(api, params=None, session=None, exchange=None):
        if not params:
            params = MockParams[api_request_name].value
            return func(api, params, session, exchange)
        else:
            return func(api, params, session, exchange)
    return api_request


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
