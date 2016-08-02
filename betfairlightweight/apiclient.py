from .baseclient import BaseClient
from .endpoints import (
    Login, Logout, KeepAlive, Betting, Account, Navigation, Scores, InPlayService, Streaming
)


class APIClient(BaseClient):

    def __init__(self, username, password, app_key=None, certs=None, locale=None):
        super(APIClient, self).__init__(username, password, app_key=app_key, certs=certs, locale=locale)

        self.login = Login(self)
        self.keep_alive = KeepAlive(self)
        self.logout = Logout(self)
        self.betting = Betting(self)
        self.account = Account(self)
        self.navigation = Navigation(self)
        self.scores = Scores(self)
        self.streaming = Streaming(self)
        self.in_play_service = InPlayService(self)
