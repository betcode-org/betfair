import json
import logging
import datetime
from requests.exceptions import ConnectionError
from betfairlightweight.errors.apiexceptions import APIError, LogoutError, LoginError, KeepAliveError


class APIMethod:

    def __init__(self, api_client, method=None, params=None, exchange=None):
        self._api_client = api_client
        self.url = None
        self.payload = None
        self.method = method
        self.params = params
        self.exchange = exchange
        self.instructions_length = 0

    @property
    def create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': self.method,
                   'params': self.params,
                   'id': 1}
        return json.dumps(payload)

    def call(self, session=None):
        date_time_sent = datetime.datetime.now()
        if not session:
            session = self._api_client.request
        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self._api_client.check_transaction_count(self.instructions_length)
        if self._api_client.check_session():
            KeepAlive(self._api_client).call()
        try:
            response = session.post(self.url, data=self.create_req, headers=self._api_client.request_headers,
                                    timeout=(3.05, 12))
        except ConnectionError:
            raise APIError(None, self.params, self.method, 'ConnectionError')
        except Exception as e:
            raise APIError(None, self.params, self.method, e)
        if response.status_code == 200:
            return response.json(), response, date_time_sent
        else:
            raise APIError(response, self.params, self.method)


class Login(APIMethod):

    def __init__(self, api_client):
        super(Login, self).__init__(api_client)
        self.url = self._api_client.URL['login']

    def call(self, session=None):
        if not session:
            session = self._api_client.request
        self.payload = 'username=' + self._api_client.username + '&password=' + self._api_client.password
        response = session.post(self.url, data=self.payload, headers=self._api_client.login_headers,
                                cert=self._api_client.cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['loginStatus'] == 'SUCCESS':
                logging.info('Login: %s' % response_json['loginStatus'])
                self._api_client.set_session_token(response_json['sessionToken'])
            return response_json
        else:
            raise LoginError(response)


class KeepAlive(APIMethod):

    def __init__(self, api_client):
        super(KeepAlive, self).__init__(api_client)
        self.url = self._api_client.URL['keep_alive']

    def call(self, session=None):
        if not session:
            session = self._api_client.request
        response = session.post(self.url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == 'SUCCESS':
                logging.info('KeepAlive: %s' % response_json['status'])
                self._api_client.set_session_token(response_json['token'])
            return response_json
        else:
            raise KeepAliveError(response)


class Logout(APIMethod):

    def __init__(self, api_client):
        super(Logout, self).__init__(api_client)
        self.url = self._api_client.URL['logout']

    def call(self, session=None):
        if not session:
            session = self._api_client.request
        response = session.get(self.url, headers=self._api_client.keep_alive_headers, cert=self._api_client.cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == 'SUCCESS':
                logging.info('Logout: %s' % response_json['status'])
                self._api_client.logout()
            return response_json
        else:
            raise LogoutError(response)


class BettingRequest(APIMethod):

    def __init__(self, api_client, method, params, exchange):
        super(BettingRequest, self).__init__(api_client, method, params, exchange)
        if not self.exchange:
            self.exchange = self._api_client.exchange
        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self.instructions_length = len(self.params['instructions'])
        if self.exchange == 'AUS':
            self.url = self._api_client.URL_AUS['betting']
        else:
            self.url = self._api_client.URL['betting']


class AccountRequest(APIMethod):

    def __init__(self, api_client, method, params, exchange):
        super(AccountRequest, self).__init__(api_client, method, params, exchange)
        if not self.exchange:
            self.exchange = self._api_client.exchange
        if self.exchange == 'AUS':
            self.url = self._api_client.URL_AUS['account']
        else:
            self.url = self._api_client.URL['account']


class ScoresRequest(APIMethod):

    def __init__(self, api_client, method, params):
        super(ScoresRequest, self).__init__(api_client, method, params)
        self.url = self._api_client.URL['scores']


class NavigationRequest:

    def __init__(self, api_client, params):
        self._api_client = api_client
        self.params = params
        self.url = self._api_client.NAVIGATION[params]

    def call(self):
        date_time_sent = datetime.datetime.now()
        headers = self._api_client.request_headers
        try:
            response = self._api_client.request.get(self.url, headers=headers, timeout=(3.05, 12))
        except Exception as e:
            raise APIError(None, self.params, e)
        if response.status_code == 200:
            json_response = response.json()
            return json_response, response, date_time_sent
        else:
            raise APIError(None, self.params)
