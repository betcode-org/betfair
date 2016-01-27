import json
import logging


class APIMethod:

    def __init__(self, api_client):
        self._api_client = api_client
        self.url = None
        self.payload = None
        self.method = None
        self.params = None
        self.instructions_length = 0

    def create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': self.method,
                   'params': self.params,
                   'id': 1}
        self.payload = json.dumps(payload)
        return self.payload

    def call(self):
        self._api_client.check_transaction_count(self.instructions_length)
        headers = self._api_client.request_headers
        response = self._api_client.request.post(self.url, data=self.payload, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            return json_response
        else:
            logging.error('Requests error: %s' % response.status_code)


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
                logging.info('Login: %s', response_json['loginStatus'])
                self._api_client.set_session_token(response_json['sessionToken'])
            return response_json
        else:
            logging.error('Requests login error: %s' % response.status_code)


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
                logging.info('KeepAlive: %s', response_json['status'])
                self._api_client.set_session_token(response_json['token'])
            return response_json
        else:
            logging.error('Requests keepALive error: %s' % response.status_code)


class Logout(APIMethod):

    def __init__(self, api_client):
        super(Logout, self).__init__(api_client)
        self.url = self._api_client.URL['logout']

    def call(self):
        headers = self._api_client.keep_alive_headers
        cert = self._api_client.cert
        response = self._api_client.request.get(self.url, headers=headers, cert=cert)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['status'] == 'SUCCESS':
                logging.info('Logout: %s', response_json['status'])
                self._api_client.logout()
            return response_json
        else:
            logging.error('Requests logout error: %s' % response.status_code)


class BettingRequest(APIMethod):

    def __init__(self, api_client, method, params):
        super(BettingRequest, self).__init__(api_client)
        self.method = method
        self.params = params
        if self.method in ['SportsAPING/v1.0/placeOrders', 'SportsAPING/v1.0/replaceOrders']:
            self.instructions_length = len(self.params['instructions'])
        self.url = self._api_client.URL['betting']
        self.create_req()


class AccountRequest(APIMethod):

    def __init__(self, api_client, method, params):
        super(AccountRequest, self).__init__(api_client)
        self.method = method
        self.params = params
        self.url = self._api_client.URL['account']
        self.create_req()
