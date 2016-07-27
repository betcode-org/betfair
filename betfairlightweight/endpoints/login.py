
from .base import BaseEndpoint
from ..exceptions import LoginError, APIError
from ..utils import check_status_code


class Login(BaseEndpoint):

    _error = LoginError

    def __call__(self):
        data = 'username=' + self.client.username + '&password=' + self.client.password
        url = '%s%s' % (self.client.identity_uri, 'certlogin')
        response = self.request(url, data)

        response_json = response.json()
        self.client.set_session_token(response_json.get('sessionToken'))
        return response_json

    def request(self, url, data=None, params=None, session=None):
        if not session:
            session = self.client.session

        try:
            response = session.post(url, data=data, headers=self.client.login_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, params, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, params, exception=e)

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json(), params)
        return response

    def _error_handler(self, response, params=None, method=None):
        if response.get('loginStatus') != 'SUCCESS':
            raise self._error(response)
