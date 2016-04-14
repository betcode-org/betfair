import json
import datetime
from requests.exceptions import ConnectionError

from .errors import apierrorhandling
from .errors.apiexceptions import APIError, LogoutError, LoginError, KeepAliveError


class APIMethod:
    """ This is the base class for all api requests """

    _error_handler = staticmethod(apierrorhandling.api_betting_error_handling)
    _error = APIError

    def __init__(self, api_client, method=None, params=None, exchange=None):
        """
        :param api_client:
            Client to be used for request.
        :param method:
            Betfair api-ng method to be used.
        :param params:
            Params to be used in requests, if None will use MockParams Enum.
        :param exchange:
            Allows to specify exchange to be used, regardless of client.exchange.
        """
        self._api_client = api_client
        self.payload = None
        self.method = method
        self.params = params
        self.exchange = exchange
        self.instructions_length = 0

        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            instructions = self.params.get('instructions')
            if instructions:
                self.instructions_length = len(self.params.get('instructions'))

    def __call__(self, session=None):
        url = self._api_client.get_url(self.__class__.__name__, self.exchange)
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self._api_client.check_transaction_count(self.instructions_length)
        try:
            response = session.post(url, data=self.create_req, headers=self._api_client.request_headers,
                                    timeout=(3.05, 12))
        except ConnectionError:
            raise APIError(None, self.params, self.method, 'ConnectionError')
        except Exception as e:
            raise APIError(None, self.params, self.method, e)
        return self.create_resp(response, date_time_sent)

    def create_resp(self, response, date_time_sent):
        if response.status_code == 200:
            self._error_handler(response.json(), self.params, self.method)
            return response.json(), response, date_time_sent
        else:
            raise self._error(response, self.params, self.method)

    @property
    def create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': self.method,
                   'params': self.params,
                   'id': 1}
        return json.dumps(payload)


class Login(APIMethod):
    """ Login method """
    _error_handler = staticmethod(apierrorhandling.api_login_error_handling)
    _error = LoginError

    def __call__(self, session=None):
        url = self._api_client.get_url(self.__class__.__name__, self.exchange)
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        self.payload = 'username=' + self._api_client.username + '&password=' + self._api_client.password
        response = session.post(url, data=self.payload, headers=self._api_client.login_headers,
                                cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class KeepAlive(APIMethod):
    """ KeepAlive method """
    _error_handler = staticmethod(apierrorhandling.api_keep_alive_error_handling)
    _error = KeepAliveError

    def __call__(self, session=None):
        url = self._api_client.get_url(self.__class__.__name__, self.exchange)
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        response = session.post(url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class Logout(APIMethod):
    """ Logout method """
    _error_handler = staticmethod(apierrorhandling.api_logout_error_handling)
    _error = LogoutError

    def __call__(self, session=None):
        url = self._api_client.get_url(self.__class__.__name__, self.exchange)
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        response = session.get(url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class BettingRequest(APIMethod):
    """ Betting method """
    pass


class OrderRequest(APIMethod):
    """ Order method """
    _error_handler = staticmethod(apierrorhandling.api_order_error_handling)


class AccountRequest(APIMethod):
    """ Account method """
    pass


class ScoresRequest(APIMethod):
    """ Scores method """
    pass


class NavigationRequest(APIMethod):
    """ Navigation method """

    def __call__(self, session=None):
        url = self._api_client.get_url(self.__class__.__name__, self.exchange)
        date_time_sent = datetime.datetime.now()
        headers = self._api_client.request_headers
        try:
            response = self._api_client.request.get(url, headers=headers, timeout=(3.05, 12))
        except Exception as e:
            raise APIError(None, self.params, e)
        return self.create_resp(response, date_time_sent)
