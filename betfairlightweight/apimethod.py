import json
import datetime
from requests.exceptions import ConnectionError
from .errors import apierrorhandling
from .errors.apiexceptions import APIError, LogoutError, LoginError, KeepAliveError, BetfairError


class APIMethod:
    """ This is the base class for all api requests """

    def __init__(self, api_client, method=None, params=None, exchange=None):
        """
        :param api_client:
            Client to be used for request.
        :param method:
            Betfair api-ng method to be used.
        :param params:
            Params to be used in requests, if None will use MockParams Enum.
        :param exchange:
            Allows to specify certain exchange to be used, regardless of client.exchange.
        """
        self._api_client = api_client
        self.url = None
        self.payload = None
        self.method = method
        self.params = params
        self.exchange = exchange
        self.error = APIError
        self.error_handler = apierrorhandling.api_betting_error_handling
        self.instructions_length = 0

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self._api_client.check_transaction_count(self.instructions_length)
        try:
            response = session.post(self.url, data=self.create_req, headers=self._api_client.request_headers,
                                    timeout=(3.05, 12))
        except ConnectionError:
            raise APIError(None, self.params, self.method, 'ConnectionError')
        except Exception as e:
            raise APIError(None, self.params, self.method, e)
        return self.create_resp(response, date_time_sent)

    def create_resp(self, response, date_time_sent):
        if response.status_code == 200:
            self.error_handler(response.json(), self.params, self.method)
            return response.json(), response, date_time_sent
        else:
            raise self.error(response, self.params, self.method)

    def initiate_exchange(self, call_type):
        if not self.exchange:
            self.exchange = self._api_client.exchange
        if self.exchange == 'UK' or call_type in ['login', 'keep_alive', 'logout']:
            url = self._api_client.URL[call_type]
        elif self.exchange == 'AUS':
            url = self._api_client.URL_AUS[call_type]
        else:
            raise BetfairError
        return url

    @property
    def create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': self.method,
                   'params': self.params,
                   'id': 1}
        return json.dumps(payload)


class Login(APIMethod):
    """ Login method """

    def __init__(self, api_client):
        super(Login, self).__init__(api_client)
        self.url = self.initiate_exchange('login')
        self.error = LoginError
        self.error_handler = apierrorhandling.api_login_error_handling

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        self.payload = 'username=' + self._api_client.username + '&password=' + self._api_client.password
        response = session.post(self.url, data=self.payload, headers=self._api_client.login_headers,
                                cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class KeepAlive(APIMethod):
    """ KeepAlive method """

    def __init__(self, api_client):
        super(KeepAlive, self).__init__(api_client)
        self.url = self.initiate_exchange('keep_alive')
        self.error = KeepAliveError
        self.error_handler = apierrorhandling.api_keep_alive_error_handling

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        response = session.post(self.url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class Logout(APIMethod):
    """ Logout method """

    def __init__(self, api_client):
        super(Logout, self).__init__(api_client)
        self.url = self.initiate_exchange('logout')
        self.error = LogoutError
        self.error_handler = apierrorhandling.api_logout_error_handling

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        response = session.get(self.url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        return self.create_resp(response, date_time_sent)


class BettingRequest(APIMethod):
    """ Betting method """

    def __init__(self, api_client, method, params, exchange):
        super(BettingRequest, self).__init__(api_client, method, params, exchange)
        self.url = self.initiate_exchange('betting')


class OrderRequest(APIMethod):
    """ Order method """

    def __init__(self, api_client, method, params, exchange):
        super(OrderRequest, self).__init__(api_client, method, params, exchange)
        instructions = self.params.get('instructions')
        if instructions and self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self.instructions_length = len(self.params.get('instructions'))
        self.url = self.initiate_exchange('betting')
        self.error_handler = apierrorhandling.api_order_error_handling


class AccountRequest(APIMethod):
    """ Account method """

    def __init__(self, api_client, method, params, exchange):
        super(AccountRequest, self).__init__(api_client, method, params, exchange)
        self.url = self.initiate_exchange('account')


class ScoresRequest(APIMethod):
    """ Scores method """

    def __init__(self, api_client, method, params):
        super(ScoresRequest, self).__init__(api_client, method, params)
        self.url = self.initiate_exchange('scores')


class NavigationRequest(APIMethod):
    """ Navigation method """

    def __init__(self, api_client, params):
        super(NavigationRequest, self).__init__(api_client, method=None, params=params)
        self._api_client = api_client
        self.params = params
        self.url = self.initiate_exchange('NAVIGATION')

    def __call__(self, session=None):
        date_time_sent = datetime.datetime.now()
        headers = self._api_client.request_headers
        try:
            response = self._api_client.request.get(self.url, headers=headers, timeout=(3.05, 12))
        except Exception as e:
            raise APIError(None, self.params, e)
        return self.create_resp(response, date_time_sent)
