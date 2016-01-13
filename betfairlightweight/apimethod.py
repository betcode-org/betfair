import json


class APIMethod:

    def __init__(self, api_client):
        self._api_client = api_client
        self.url = None
        self.payload = None
        self.method = None
        self.params = None

    def create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': self.method,
                   'params': self.params,
                   'id': 1}
        self.payload = json.dumps(payload)
        return self.payload

    def call(self):
        if self._api_client.check_transaction_count(self.method):
            headers = self._api_client.request_headers
            response = self._api_client.request.post(self.url, data=self.payload, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
                return json_response
            else:
                print('request error:', response.status_code)
        else:
            print('Transaction limit reached:', self._api_client.transaction_count)


class Login(APIMethod):

    def __init__(self, api_client):
        super(Login, self).__init__(api_client)
        self.url = self._api_client.URL['login']

    def call(self):
        self.payload = 'username=' + self._api_client.username + '&password=' + self._api_client.password
        headers = self._api_client.login_headers
        cert = self._api_client.cert
        response = self._api_client.request.post(self.url, data=self.payload, headers=headers, cert=cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['loginStatus'] == 'SUCCESS':
                self._api_client.set_session_token(response_json['sessionToken'])
        else:
            print('login error:', response.status_code)


class KeepAlive(APIMethod):

    def __init__(self, api_client):
        super(KeepAlive, self).__init__(api_client)
        self.url = self._api_client.URL['keep_alive']

    def call(self):
        headers = self._api_client.keep_alive_headers
        cert = self._api_client.cert
        response = self._api_client.request.post(self.url, headers=headers, cert=cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == 'SUCCESS':
                self._api_client.set_session_token(response_json['token'])
        else:
            print('login error:', response.status_code)


class BettingRequest(APIMethod):

    def __init__(self, api_client, method, params):
        super(BettingRequest, self).__init__(api_client)
        self.method = method
        self.params = params
        self.url = self._api_client.URL['betting']
        self.create_req()


class AccountRequest(APIMethod):

    def __init__(self, api_client, method, params):
        super(AccountRequest, self).__init__(api_client)
        self.method = method
        self.params = params
        self.url = self._api_client.URL['account']
        self.create_req()


def login(api):
    return Login(api).call()


def keep_alive(api):
    return KeepAlive(api).call()


# Betting requests


def list_event_types(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()


def list_competitions(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call()


def list_time_ranges(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call()


def list_events(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call()


def list_market_types(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call()


def list_countries(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call()


def list_venues(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call()


def list_market_catalogue(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call()


def list_market_book(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call()


def place_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/placeOrders', params).call()


def cancel_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/cancelOrders', params).call()


def update_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/updateOrders', params).call()


def replace_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/replaceOrders', params).call()


def list_current_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params).call()


def list_cleared_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params).call()


def list_market_profit_and_loss(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params).call()


# account requests


def get_account_funds(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params).call()


def get_account_details(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params).call()


def get_account_statement(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params).call()


def list_currency_rates(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params).call()


def transfer_funds(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params).call()
