import requests
import datetime
import os

from .errors.apiexceptions import AppKeyError


class BaseClient:

    def __init__(self, username, password, app_key=None, exchange='UK'):
        """
        :param username:
            Betfair username.
        :param password:
            Password for supplied username.
        :param app_key:
            App Key for account, if None will look in .bashprofile
        :param exchange:
            Allows to specify exchange to be used, UK or AUS.
        """
        self.username = username
        self.password = password
        self.app_key = app_key
        self.exchange = exchange

        self.session = requests
        self._login_time = None
        self._next_hour = None
        self.session_token = None

        self.get_app_key()

    def set_session_token(self, session_token):
        self.session_token = session_token
        self._login_time = datetime.datetime.now()

    def get_app_key(self):
        if self.app_key is None:
            if os.environ.get(self.username):
                self.app_key = os.environ.get(self.username)
            else:
                raise AppKeyError(self.username)

    def client_logout(self):
        self.session_token = None
        self._login_time = None

    @property
    def session_expired(self):
        if not self._login_time or (datetime.datetime.now()-self._login_time).total_seconds() > 12000:
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
                'X-Application': self.app_key,
                'X-Authentication': self.session_token,
                'content-type': 'application/x-www-form-urlencoded'}

    @property
    def request_headers(self):
        return {'X-Application': self.app_key,
                'X-Authentication': self.session_token,
                'content-type': 'application/json'}
