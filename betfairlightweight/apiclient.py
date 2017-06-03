from .baseclient import BaseClient
from . import endpoints


class APIClient(BaseClient):

    def __init__(self, username, password=None, app_key=None, certs=None, locale=None, cert_files=None,
                 lightweight=False):
        """
        Creates API client for API operations.

        :param str username: Betfair username
        :param str password: Password for supplied username, if None will look in .bashprofile
        :param str app_key: App Key for account, if None will look in .bashprofile
        :param str certs: Directory for certificates, if None will look in /certs/
        :param str locale: Exchange to be used, defaults to UK for login and global for api
        :param list cert_files: Certificate and key files. If None will look in `certs`
        :param bool lightweight: If True endpoints will return dict not a resource (22x faster)
        """
        super(APIClient, self).__init__(
            username, password, app_key=app_key, certs=certs, locale=locale, cert_files=cert_files,
            lightweight=lightweight
        )

        self.login = endpoints.Login(self)
        self.keep_alive = endpoints.KeepAlive(self)
        self.logout = endpoints.Logout(self)
        self.betting = endpoints.Betting(self)
        self.account = endpoints.Account(self)
        self.navigation = endpoints.Navigation(self)
        self.scores = endpoints.Scores(self)
        self.streaming = endpoints.Streaming(self)
        self.in_play_service = endpoints.InPlayService(self)
        self.race_card = endpoints.RaceCard(self)
        self.historical = endpoints.Historical(self)

    def __repr__(self):
        return '<APIClient [%s]>' % self.username

    def __str__(self):
        return 'APIClient'
