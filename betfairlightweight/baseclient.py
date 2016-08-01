import requests
import collections
import datetime
import os

from .exceptions import AppKeyError, CertsError


class BaseClient:

    IDENTITY_URLS = collections.defaultdict(
            lambda: 'https://identitysso.betfair.com/api/',
            spain='https://identitysso.betfair.es',
            italy='https://identitysso.betfair.it/api/',
            romania='https://idenititysso.betfair.ro',
            w_con='https://identitysso.w-con.betfair.com',
            europe='https://identitysso.betfaironline.eu',
    )

    API_URLS = collections.defaultdict(
            lambda: 'https://api.betfair.com/exchange/betting/json-rpc/v1',
            australia='https://api-au.betfair.com/exchange/betting/json-rpc/v1',
    )

    NAVIGATION_URLS = collections.defaultdict(
            lambda: 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
            spain='https://api.betfair.es/exchange/betting/rest/v1/en/navigation/menu.json',
            italy='https://api.betfair.it/exchange/betting/rest/v1/en/navigation/menu.json'
    )

    def __init__(self, username, password, app_key=None, certs=None, locale=None):
        """
        :param username:
            Betfair username.
        :param password:
            Password for supplied username.
        :param app_key:
            App Key for account, if None will look in .bashprofile
        :param certs:
            Directory for certificates, if None will look in /certs/
        :param locale:
            Exchange to be used, defaults to UK for login and global for api.
        """
        self.username = username
        self.password = password
        self.app_key = app_key
        self.certs = certs
        self.locale = locale

        self.session = requests
        self._login_time = None
        self.session_token = None
        self.identity_uri = self.IDENTITY_URLS[locale]
        self.api_uri = self.API_URLS[locale]
        self.navigation_uri = self.NAVIGATION_URLS[locale]

        self.get_app_key()

    def set_session_token(self, session_token):
        """Sets session token and new login time.
        :param session_token: Session token from request.
        """
        self.session_token = session_token
        self._login_time = datetime.datetime.now()

    def get_app_key(self):
        """If app_key is not set will look in environment
        variables for username
        """
        if self.app_key is None:
            if os.environ.get(self.username):
                self.app_key = os.environ.get(self.username)
            else:
                raise AppKeyError(self.username)

    def client_logout(self):
        """Resets session token and login time.
        """
        self.session_token = None
        self._login_time = None

    @property
    def session_expired(self):
        """Returns True if login_time not set or seconds since
        login time is greater than 200 mins.
        """
        if not self._login_time or (datetime.datetime.now()-self._login_time).total_seconds() > 12000:
            return True

    @property
    def cert(self):
        """Looks in /certs/ for betfair certs.
        :return: Path of cert files
        """
        certs = self.certs or '/certs/'
        cert_paths = []
        ssl_path = os.path.join(os.pardir, certs)
        try:
            cert_path = os.listdir(ssl_path)
        except FileNotFoundError:
            raise CertsError
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
