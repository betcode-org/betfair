import requests

from .baseclient import BaseClient
from . import endpoints


class APIClient(BaseClient):
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
        Creates API client for API operations.

        :param str username: Betfair username
        :param str password: Betfair password for supplied username, if None will look in .bashprofile
        :param str app_key: App Key for account, if None will look in .bashprofile
        :param str certs: Directory for certificates, if None will look in /certs
        :param str locale: Exchange to be used, defaults to international (.com) exchange
        :param list cert_files: Certificate and key files. If None will use `self.certs`
        :param bool lightweight: If True endpoints will return dict not a resource (22x faster)
        :param requests.Session session: Pass requests session object, defaults to a new request each request
        """
        super(APIClient, self).__init__(
            username,
            password,
            app_key=app_key,
            certs=certs,
            locale=locale,
            cert_files=cert_files,
            lightweight=lightweight,
            session=session,
        )

        self.login = endpoints.Login(self)
        self.login_interactive = endpoints.LoginInteractive(self)
        self.keep_alive = endpoints.KeepAlive(self)
        self.logout = endpoints.Logout(self)
        self.betting = endpoints.Betting(self)
        self.account = endpoints.Account(self)
        self.navigation = endpoints.Navigation(self)
        self.scores = endpoints.Scores(self)
        self.streaming = endpoints.Streaming(self)
        self.in_play_service = endpoints.InPlayService(self)
        self.race_card = endpoints.RaceCard(self)
        self.historic = endpoints.Historic(self)

    def __repr__(self) -> str:
        return "<APIClient [%s]>" % self.username

    def __str__(self) -> str:
        return "APIClient"
