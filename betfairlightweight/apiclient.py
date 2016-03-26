import datetime
import os
import requests
import logging
import threading
from betfairlightweight.errors.apiexceptions import AppKeyError, TransactionCountError


class APIClient:

    URL = {'login': 'https://identitysso.betfair.com/api/certlogin',
           'logout': 'https://identitysso.betfair.com/api/logout',
           'keep_alive': 'https://identitysso.betfair.com/api/keepAlive',
           'betting': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
           'scores': 'https://api.betfair.com/exchange/scores/json-rpc/v1',
           'account': 'https://api.betfair.com/exchange/account/json-rpc/v1'}

    URL_AUS = {'betting': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
               'account': 'https://api-au.betfair.com/exchange/account/json-rpc/v1'}

    NAVIGATION = {'UK': 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
                  'ITALY': 'https://api.betfair.it/exchange/betting/rest/v1/en/navigation/menu.json',
                  'SPAIN': 'https://api.betfair.es/exchange/betting/rest/v1/en/navigation/menu.json'}

    TRANSACTION_LIMIT = 999

    def __init__(self, username, password, exchange='UK'):
        self.username = username
        self.password = password
        self.exchange = exchange
        now = datetime.datetime.now()
        self.time_trig = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        self.login_time = None
        self.session_lock = threading.Lock
        self._session_token = None
        self.request = requests
        self.transaction_count = 0
        self.app_key = self.get_app_key()

    def set_session_token(self, session_token, keep_alive=False):
        self._session_token = session_token
        if not keep_alive:
            self.transaction_count = 0
        self.login_time = datetime.datetime.now()
        logging.info('New sessionToken: %s', self._session_token)

    def check_session(self):  # todo thread lock
        if not self.login_time or (datetime.datetime.now()-self.login_time).total_seconds() > 12000:
            return True

    def check_transaction_count(self, count):
        now = datetime.datetime.now()
        if now > self.time_trig:
            logging.info('Transaction count reset: %s', self.transaction_count)
            self.time_trig = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            self.transaction_count = 0
        self.transaction_count += count
        if self.transaction_count > self.TRANSACTION_LIMIT:
            logging.error('Transaction limit reached: %s', self.transaction_count)
            raise TransactionCountError

    def logout(self):
        self._session_token = None
        self.login_time = None

    def get_app_key(self):
        app_key = os.environ.get(self.username)
        logging.info('App key found for %s: %s' % (self.username, app_key))
        if app_key:
            return os.environ.get(self.username)
        else:
            raise AppKeyError

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
