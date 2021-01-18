import os
import time
import requests
import collections

from .exceptions import PasswordError, AppKeyError, CertsError
from .utils import default_user_agent

IDENTITY = "https://identitysso.betfair{tld}/api/"
IDENTITY_CERT = "https://identitysso-cert.betfair{tld}/api/"
API = "https://api.betfair.com/exchange/"
NAVIGATION = (
    "https://api.betfair{tld}/exchange/betting/rest/v1/{locale}/navigation/menu.json"
)
USER_AGENT = default_user_agent()


class BaseClient:
    """
    Base API client
    """

    IDENTITY_URLS = collections.defaultdict(
        lambda: IDENTITY.format(tld=".com"),
        spain=IDENTITY.format(tld=".es"),
        italy=IDENTITY.format(tld=".it"),
        romania=IDENTITY.format(tld=".ro"),
        sweden=IDENTITY.format(tld=".se"),
        australia=IDENTITY.format(tld=".com.au"),
    )

    IDENTITY_CERT_URLS = collections.defaultdict(
        lambda: IDENTITY_CERT.format(tld=".com"),
        spain=IDENTITY_CERT.format(tld=".es"),
        italy=IDENTITY_CERT.format(tld=".it"),
        romania=IDENTITY_CERT.format(tld=".ro"),
        sweden=IDENTITY_CERT.format(tld=".se"),
    )

    API_URLS = collections.defaultdict(lambda: API)

    NAVIGATION_URLS = collections.defaultdict(
        lambda: NAVIGATION.format(tld=".com", locale="en"),
        spain=NAVIGATION.format(tld=".es", locale="es"),
        italy=NAVIGATION.format(tld=".it", locale="it"),
    )

    SESSION_TIMEOUT = collections.defaultdict(lambda: 24 * 60 * 60, italy=20 * 60)

    def __init__(
        self,
        username: str,
        password: str = None,
        app_key: str = None,
        certs: str = None,
        locale: str = None,
        cert_files: list = None,
        lightweight: bool = False,
        session: requests.Session = None,
    ):
        """
        Creates base client for API operations.

        :param str username: Betfair username
        :param str password: Betfair password for supplied username, if None will look in .bashprofile
        :param str app_key: App Key for account, if None will look in .bashprofile
        :param str certs: Directory for certificates, if None will look in /certs
        :param str locale: Exchange to be used, defaults to international (.com) exchange
        :param list cert_files: Certificate and key files. If None will use `self.certs`
        :param bool lightweight: If True endpoints will return dict not a resource (22x faster)
        :param requests.Session session: Pass requests session object, defaults to a new request each request
        """
        self.username = username
        self.password = password
        self.app_key = app_key
        self.certs = certs
        self.locale = locale
        self.cert_files = cert_files
        self.lightweight = lightweight

        self.session = session if session else requests
        self._login_time = None
        self.session_token = None
        self.identity_uri = self.IDENTITY_URLS[locale]
        self.identity_cert_uri = self.IDENTITY_CERT_URLS[locale]
        self.api_uri = self.API_URLS[locale]
        self.navigation_uri = self.NAVIGATION_URLS[locale]
        self.session_timeout = self.SESSION_TIMEOUT[locale]

        self.get_password()
        self.get_app_key()

    def set_session_token(self, session_token: str) -> None:
        """
        Sets session token and new login time.

        :param str session_token: Session token from request.
        """
        self.session_token = session_token
        self._login_time = time.time()

    def get_password(self) -> str:
        """
        If password is not provided will look in environment variables
        for self.username+'password'.
        """
        if self.password is None:
            if os.environ.get(self.username + "password"):
                self.password = os.environ.get(self.username + "password")
            else:
                raise PasswordError(self.username)
        return self.password

    def get_app_key(self) -> str:
        """
        If app_key is not provided will look in environment
        variables for username.
        """
        if self.app_key is None:
            if os.environ.get(self.username):
                self.app_key = os.environ.get(self.username)
            else:
                raise AppKeyError(self.username)
        return self.app_key

    def client_logout(self) -> None:
        """
        Resets session token and login time.
        """
        self.session_token = None
        self._login_time = None

    @property
    def session_expired(self) -> bool:
        """
        Returns True if login_time not set or seconds since
        login time is greater half session timeout.
        """
        if not self._login_time or time.time() - self._login_time > (
            self.session_timeout / 2
        ):
            return True
        else:
            return False

    @property
    def cert(self) -> list:
        """
        The betfair certificates, by default it looks for the
        certificates in /certs/.

        :return: Path of cert files
        :rtype: str
        """
        if self.cert_files is not None:
            return self.cert_files

        certs = self.certs or "/certs/"
        ssl_path = os.path.join(os.pardir, certs)
        try:
            cert_path = os.listdir(ssl_path)
        except FileNotFoundError as e:
            raise CertsError(str(e))

        cert = None
        key = None
        for file in cert_path:
            ext = os.path.splitext(file)[-1]
            if ext in [".crt", ".cert"]:
                cert = os.path.join(ssl_path, file)
            elif ext == ".key":
                key = os.path.join(ssl_path, file)
        if cert is None or key is None:
            raise CertsError(
                "Certificates not found in directory: '%s' (make sure .crt and .key file is present)"
                % ssl_path
            )
        return [cert, key]

    @property
    def login_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "X-Application": self.app_key,
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        }

    @property
    def keep_alive_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "X-Application": self.app_key,
            "X-Authentication": self.session_token,
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        }

    @property
    def request_headers(self) -> dict:
        return {
            "X-Application": self.app_key,
            "X-Authentication": self.session_token,
            "content-type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": USER_AGENT,
        }
