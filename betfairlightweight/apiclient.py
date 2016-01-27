import datetime
import os
import requests
import logging
from betfairlightweight.secret import APP_KEYS
from betfairlightweight.errors import apiexceptions


class APIClient:

    URL = {'login': 'https://identitysso.betfair.com/api/certlogin',
           'logout': 'https://identitysso.betfair.com/api/logout',
           'keep_alive': 'https://identitysso.betfair.com/api/keepAlive',
           'betting': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
           'account': 'https://api.betfair.com/exchange/account/json-rpc/v1'}

    URL_AUS = {'betting': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
               'account': 'https://api-au.betfair.com/exchange/account/json-rpc/v1'}  # todo integrate

    __APP_KEYS = APP_KEYS  # APP_KEYS = {'username': appKey}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        now = datetime.datetime.now()
        self.time_trig = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        self.login_time = None
        self._session_token = None
        self._appKey = None
        self.request = requests.session()
        self.transaction_count = 0

    def set_session_token(self, session_token):
        self._session_token = session_token
        self.transaction_count = 0
        self.login_time = datetime.datetime.now()
        logging.info('New sessionToken: %s', self._session_token)

    def check_transaction_count(self, count):
        now = datetime.datetime.now()
        if now > self.time_trig:
            logging.info('Transaction count reset: %s', self.transaction_count)
            self.time_trig = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            self.transaction_count = 0
        self.transaction_count += count
        if self.transaction_count > 999:
            logging.error('Transaction limit reached: %s', self.transaction_count)
            raise apiexceptions.TransactionCountError

    def logout(self):
        self._session_token = None
        self.login_time = None

    @property
    def app_key(self):
        return self.__APP_KEYS[self.username]

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
        headers = {'X-Application': 1,
                   'content-type': 'application/x-www-form-urlencoded'}
        return headers

    @property
    def keep_alive_headers(self):
        headers = {'Accept': 'application/json',
                   'X-Application': self.app_key,
                   'X-Authentication': self._session_token,
                   'content-type': 'application/x-www-form-urlencoded'}
        return headers

    @property
    def request_headers(self):
        headers = {'X-Application': self.app_key,
                   'X-Authentication': self._session_token,
                   'content-type': 'application/json'}
        return headers
