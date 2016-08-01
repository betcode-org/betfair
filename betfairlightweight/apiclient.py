from .baseclient import BaseClient
from .endpoints import (
    Login, Logout, KeepAlive, Betting, Account, Navigation, Scores, InPlayService
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
        self.in_play_service = InPlayService(self)


# class BaseClient:
#     """This class is a container for all client options. It's
#     primary purpose is to hold appkeys, session tokens, urls,
#     transaction count, provide headers for requests and make
#     requests to betfair
#     """
#
#     __url = {'Login': 'https://identitysso.betfair.com/api/certlogin',
#              'Logout': 'https://identitysso.betfair.com/api/logout',
#              'KeepAlive': 'https://identitysso.betfair.com/api/keepAlive',
#              'BettingRequest': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
#              'OrderRequest': 'https://api.betfair.com/exchange/betting/json-rpc/v1',
#              'ScoresRequest': 'https://api.betfair.com/exchange/scores/json-rpc/v1',
#              'AccountRequest': 'https://api.betfair.com/exchange/account/json-rpc/v1'}
#
#     __url_aus = {'BettingRequest': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
#                  'OrderRequest': 'https://api-au.betfair.com/exchange/betting/json-rpc/v1',
#                  'ScoresRequest': None,
#                  'AccountRequest': 'https://api-au.betfair.com/exchange/account/json-rpc/v1'}
#
#     __navigation = {'UK': 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
#                     'AUS': 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json',
#                     'ITALY': 'https://api.betfair.it/exchange/betting/rest/v1/en/navigation/menu.json',
#                     'SPAIN': 'https://api.betfair.es/exchange/betting/rest/v1/en/navigation/menu.json'}
#
#     __scores = {'UK': 'https://www.betfair.com/inplayservice/v1/scoresAndBroadcast'}
#
#     def __init__(self, username, password, app_key=None, exchange='UK'):
#         """
#         :param username:
#             Betfair username.
#         :param password:
#             Password for supplied username.
#         :param app_key:
#             App Key for account, if None will look in .bashprofile
#         :param exchange:
#             Allows to specify exchange to be used, UK or AUS.
#         """
#         self.username = username
#         self.password = password
#         self._app_key = app_key
#         self.exchange = exchange
#         self._login_time = None
#         self.request = requests
#         self.transaction_limit = 999
#         self.transaction_count = 0
#         self._next_hour = None
#         self.set_next_hour()
#         self._session_token = None
#
#         self.get_app_key()
#
#     def set_session_token(self, session_token, call_type):
#         self._session_token = session_token
#         self._login_time = datetime.datetime.now()
#         logging.info('%s new sessionToken: %s' % (call_type, self._session_token))
#
#     def set_next_hour(self):
#         now = datetime.datetime.now()
#         self._next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
#
#     def check_transaction_count(self, count):
#         if datetime.datetime.now() > self._next_hour:
#             logging.info('Transaction count reset: %s' % self.transaction_count)
#             self.set_next_hour()
#             self.transaction_count = 0
#         self.transaction_count += count
#         if self.transaction_count > self.transaction_limit:
#             raise TransactionCountError(self.transaction_count)
#
#     def client_logout(self, response_status):
#         self._session_token = None
#         self._login_time = None
#         logging.info('Logout: %s' % response_status)
#
#     def get_app_key(self):
#         logging.info('Username: %s', self.username)
#         if self._app_key is None:
#             if os.environ.get(self.username):
#                 self._app_key = os.environ.get(self.username)
#             else:
#                 raise AppKeyError(self.username)
#
#     def get_url(self, call_type, exchange):
#         if exchange:
#             call_exchange = exchange
#         else:
#             call_exchange = self.exchange
#         if call_type == 'NavigationRequest':
#             url = self.__navigation[call_exchange]
#         elif call_type == 'ScoresBroadcastRequest':
#             url = self.__scores[call_exchange]
#         elif call_exchange == 'UK' or call_type in ['Login', 'KeepAlive', 'Logout']:
#             url = self.__url[call_type]
#         elif call_exchange == 'AUS':
#             url = self.__url_aus[call_type]
#         else:
#             raise BetfairError
#         return url
#
#     @property
#     def session_expired(self):
#         if not self._login_time or (datetime.datetime.now()-self._login_time).total_seconds() > 12000:
#             return True
#
#     @property
#     def check_session(self):
#         if self._session_token:
#             return True
#
#     @property
#     def cert(self):
#         cert_paths = []
#         ssl_path = os.path.join(os.pardir, '/certs/')
#         cert_path = os.listdir(ssl_path)
#         for file in cert_path:
#             ext = file.rpartition('.')[2]
#             if ext in ['key', 'crt', 'pem']:
#                 cert_path = ssl_path + file
#                 cert_paths.append(cert_path)
#         cert_paths.sort()
#         return cert_paths
#
#     @property
#     def login_headers(self):
#         return {'X-Application': 1,
#                 'content-type': 'application/x-www-form-urlencoded'}
#
#     @property
#     def keep_alive_headers(self):
#         return {'Accept': 'application/json',
#                 'X-Application': self._app_key,
#                 'X-Authentication': self._session_token,
#                 'content-type': 'application/x-www-form-urlencoded'}
#
#     @property
#     def request_headers(self):
#         return {'X-Application': self._app_key,
#                 'X-Authentication': self._session_token,
#                 'content-type': 'application/json'}
#
#
# class APIClient(BaseClient):
#     """
#     This class is a container for all request operations,
#     separated to make modifications easier.
#     """
#
#     def login(self):
#         request = Login(self)
#         (response, raw_response, sent) = request()
#         self.set_session_token(response.get('sessionToken'), 'Login')
#         return response
#
#     def keep_alive(self):
#         request = KeepAlive(self)
#         (response, raw_response, sent) = request()
#         self.set_session_token(response.get('token'), 'KeepAlive')
#         return response
#
#     def logout(self):
#         request = Logout(self)
#         (response, raw_response, sent) = request()
#         self.client_logout(response.get('status'))
#         return response
#
#     # Betting requests
#
#     @api_request
#     def list_event_types(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listEventTypes', params, exchange)
#         return process_request(request, session, apiparsedata.EventTypeResult)
#
#     @api_request
#     def list_competitions(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listCompetitions', params, exchange)
#         return process_request(request, session, apiparsedata.CompetitionResult)
#
#     @api_request
#     def list_time_ranges(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listTimeRanges', params, exchange)
#         return process_request(request, session, apiparsedata.TimeRangeResult)
#
#     @api_request
#     def list_events(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listEvents', params, exchange)
#         return process_request(request, session, apiparsedata.EventResult)
#
#     @api_request
#     def list_market_types(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listMarketTypes', params, exchange)
#         return process_request(request, session, apiparsedata.MarketTypeResult)
#
#     @api_request
#     def list_countries(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listCountries', params, exchange)
#         return process_request(request, session, apiparsedata.CountryResult)
#
#     @api_request
#     def list_venues(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listVenues', params, exchange)
#         return process_request(request, session, apiparsedata.VenueResult)
#
#     @api_request
#     def list_market_catalogue(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listMarketCatalogue', params, exchange)
#         return process_request(request, session, apiparsedata.MarketCatalogue)
#
#     @api_request
#     def list_market_book(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listMarketBook', params, exchange)
#         return process_request(request, session, apiparsedata.MarketBook)
#
#     # Order requests
#
#     @api_request
#     def place_orders(self, params=None, session=None, exchange=None):  # atomic
#         request = OrderRequest(self, 'SportsAPING/v1.0/placeOrders', params, exchange)
#         return process_request(request, session, apiparsebetting.PlaceOrder)
#
#     @api_request
#     def cancel_orders(self, params=None, session=None, exchange=None):
#         request = OrderRequest(self, 'SportsAPING/v1.0/cancelOrders', params, exchange)
#         if params:
#             return process_request(request, session, apiparsebetting.CancelOrder)
#         else:
#             return process_request(request, session, apiparsebetting.CancelAllOrders)
#
#     @api_request
#     def update_orders(self, params=None, session=None, exchange=None):
#         request = OrderRequest(self, 'SportsAPING/v1.0/updateOrders', params, exchange)
#         return process_request(request, session, apiparsebetting.UpdateOrder)
#
#     @api_request
#     def replace_orders(self, params=None, session=None, exchange=None):
#         request = OrderRequest(self, 'SportsAPING/v1.0/replaceOrders', params, exchange)
#         return process_request(request, session, apiparsebetting.ReplaceOrder)
#
#     @api_request
#     def list_current_orders(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listCurrentOrders', params, exchange)
#         return process_request(request, session, apiparsedata.CurrentOrders)
#
#     @api_request
#     def list_cleared_orders(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listClearedOrders', params, exchange)
#         return process_request(request, session, apiparsedata.ClearedOrders)
#
#     @api_request
#     def list_market_profit_and_loss(self, params=None, session=None, exchange=None):
#         request = BettingRequest(self, 'SportsAPING/v1.0/listMarketProfitAndLoss', params, exchange)
#         return process_request(request, session, apiparsedata.MarketProfitLoss)
#
#     @api_request
#     def list_race_status(self, params=None, session=None, exchange=None):
#         request = ScoresRequest(self, 'ScoresAPING/v1.0/listRaceDetails', params, exchange)
#         return process_request(request, session, apiparsescores.RaceStatus)
#
#     # Account requests
#
#     @api_request
#     def get_account_funds(self, params=None, session=None, exchange=None):
#         request = AccountRequest(self, 'AccountAPING/v1.0/getAccountFunds', params, exchange)
#         return process_request(request, session, apiparseaccount.AccountFunds)
#
#     @api_request
#     def get_account_details(self, params=None, session=None, exchange=None):
#         request = AccountRequest(self, 'AccountAPING/v1.0/getAccountDetails', params, exchange)
#         return process_request(request, session, apiparseaccount.AccountDetails)
#
#     @api_request
#     def get_account_statement(self, params=None, session=None, exchange=None):
#         request = AccountRequest(self, 'AccountAPING/v1.0/getAccountStatement', params, exchange)
#         return process_request(request, session, apiparseaccount.AccountStatement)
#
#     @api_request
#     def list_currency_rates(self, params=None, session=None, exchange=None):
#         request = AccountRequest(self, 'AccountAPING/v1.0/listCurrencyRates', params, exchange)
#         return process_request(request, session, apiparseaccount.CurrencyRate)
#
#     @api_request
#     def transfer_funds(self, params=None, session=None, exchange=None):
#         request = AccountRequest(self, 'AccountAPING/v1.0/transferFunds', params, exchange)
#         return process_request(request, session, apiparseaccount.TransferFunds)
#
#     # Navigation requests
#
#     def list_navigation(self, params='UK'):
#         request = NavigationRequest(self, params)
#         (response, raw_response, sent) = request()
#         return response
#
#     # Scores and Broadcasts
#
#     def list_scores(self, params=None, session=None, exchange=None):
#         request = ScoresBroadcastRequest(self, params=params, exchange=exchange)
#         return process_request(request, session, apiparsescores.Score)
#
#     # Streaming
#
#     def create_stream(self, unique_id, listener=None, timeout=6, buffer_size=1024, description='BetfairSocket'):
#         listener = listener if listener else BaseListener()
#         return BetfairStream(unique_id, listener, app_key=self._app_key, session_token=self._session_token,
#                              timeout=timeout, buffer_size=buffer_size, description=description)
