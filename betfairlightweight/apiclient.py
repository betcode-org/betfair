import datetime
import os
import requests
import logging
from .errors.apiexceptions import AppKeyError, TransactionCountError, BetfairError


class APIClient:
    """
    This class is a container for all client options. Its
    primary purpose is to hold appkeys, session tokens, urls,
    transaction count and provide headers for requests.
    """

    __url = {'Login': 'https://identitysso.betfair.com/api/certlogin',
             'Logout': 'https://identitysso.betfair.com/api/logout',
             'KeepAlive': 'https://identitysso.betfair.com/api/keepAlive',
             'BettingRequest': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
             'OrderRequest': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
             'ScoresRequest': 'https://api.betfair.com/exchange/scores/json-rpc/v1',
             'AccountRequest': 'https://api.betfair.com/exchange/account/json-rpc/v1'}

    __url_aus = {'BettingRequest': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
                 'OrderRequest': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
                 'ScoresRequest': None,
                 'AccountRequest': 'https://api-au.betfair.com/exchange/account/json-rpc/v1'}

    __navigation = {'UK': 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
                    'AUS': 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
                    'ITALY': 'https://api.betfair.it/exchange/betting/rest/v1/en/navigation/menu.json',
                    'SPAIN': 'https://api.betfair.es/exchange/betting/rest/v1/en/navigation/menu.json'}

    def __init__(self, username, password, exchange='UK'):
        """
        :param username:
            Betfair username.
        :param password:
            Password for supplied username.
        :param exchange:
            Allows to specify exchange to be used, UK or AUS.
        """
        self.username = username
        self.password = password
        self.exchange = exchange
        self.login_time = None
        self.request = requests
        self.transaction_limit = 999
        self.transaction_count = 0
        self.next_hour = None
        self.set_next_hour()
        self._session_token = None
        self._app_key = self.get_app_key()

    def set_session_token(self, session_token, call_type):
        self._session_token = session_token
        self.login_time = datetime.datetime.now()
        logging.info('%s new sessionToken: %s' % (call_type, self._session_token))

    def set_next_hour(self):
        now = datetime.datetime.now()
        self.next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    def check_transaction_count(self, count):
        if datetime.datetime.now() > self.next_hour:
            logging.info('Transaction count reset: %s' % self.transaction_count)
            self.set_next_hour()
            self.transaction_count = 0
        self.transaction_count += count
        if self.transaction_count > self.transaction_limit:
            raise TransactionCountError(self.transaction_count)

    def logout(self, response_status):
        self._session_token = None
        self.login_time = None
        logging.info('Logout: %s' % response_status)

    def get_app_key(self):
        if os.environ.get(self.username):
            return os.environ.get(self.username)
        else:
            raise AppKeyError(self.username)

    def get_url(self, call_type, exchange):
        if exchange:
            call_exchange = exchange
        else:
            call_exchange = self.exchange
        if call_type == 'NavigationRequest':
            url = self.__navigation[call_exchange]
        elif call_exchange == 'UK' or call_type in ['Login', 'KeepAlive', 'Logout']:
            url = self.__url[call_type]
        elif call_exchange == 'AUS':
            url = self.__url_aus[call_type]
        else:
            raise BetfairError
        return url

    @property
    def session_expired(self):
        if not self.login_time or (datetime.datetime.now()-self.login_time).total_seconds() > 12000:
            return True

    @property
    def cert(self):
        cert_paths = []
        ssl_path = os.path.join(os.pardir, '/certs/')
        cert_path = os.listdir(ssl_path)
        for file in cert_path:
            ext = file.rpartition('.')[2]
            if ext in ['key', 'crt', 'pem']:
                cert_path = ssl_path + file
                cert_paths.append(cert_path)
        cert_paths.sort()
        return cert_paths

    @property
    def login_headers(self):
        return {'X-Application': 1,
                'content-type': 'application/x-www-form-urlencoded'}

    @property
    def keep_alive_headers(self):
        return {'Accept': 'application/json',
                'X-Application': self._app_key,
                'X-Authentication': self._session_token,
                'content-type': 'application/x-www-form-urlencoded'}

    @property
    def request_headers(self):
        return {'X-Application': self._app_key,
                'X-Authentication': self._session_token,
                'content-type': 'application/json'}
