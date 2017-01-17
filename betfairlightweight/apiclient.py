from .baseclient import BaseClient
from . import endpoints


class APIClient(BaseClient):

    def __init__(self, username, password=None, app_key=None, certs=None, locale=None, cert_files=None):
        super(APIClient, self).__init__(username, password, app_key=app_key, certs=certs, locale=locale, cert_files=cert_files)

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

    def __repr__(self):
        return '<APIClient [%s]>' % self.username

    def __str__(self):
        return 'APIClient'
