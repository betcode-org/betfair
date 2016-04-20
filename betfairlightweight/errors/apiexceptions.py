import logging

from ..parse import enums


class BetfairError(Exception):
    """Base class for Betfair Errors"""
    pass


class AppKeyError(BetfairError):
    """Exception raised if appkey is not found"""

    def __init__(self, username):
        logging.error('AppKey not found for %s' % username)


class LoginError(BetfairError):
    """Exception raised if sessionToken is not found"""

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API login error, http error: %s' % response.status_code)
        else:
            login_status = response.get('loginStatus')
            description = enums.LoginExceptions[login_status].value
            logging.error('API login %s: %s' % (login_status, description))


class KeepAliveError(BetfairError):
    """Exception raised if session is not found"""

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API keepAlive error, http error: %s' % response.status_code)
        else:
            logging.error('API keepAlive %s: %s' % (response.get('status'), response.get('error')))


class APIError(BetfairError):
    """Exception raised if error is found"""

    def __init__(self, response, params, method=None, exception=None):
        if response is not None:
            if hasattr(response, 'status_code') and response.status_code != 200:
                logging.error('APIError, http error: %s' % response.status_code)
            else:
                code = response['error']['code']
                description = enums.GENERIC_JSON_RPC_EXCEPTIONS.get(code)
                error_details = None
                if not description:
                    error_code = response['error']['data']['APINGException']['errorCode']
                    error_details = response['error']['data']['APINGException']['errorDetails']
                    description = enums.ApingException[error_code].value
                logging.error('API betting %s: %s' % (code, description))
                logging.error('Method: %s, Parameters sent: %s' % (method, params))
                logging.error('Error details: %s' % error_details)
        else:
            logging.error('APIError error: %s' % exception)


class TransactionCountError(BetfairError):
    """Exception raised if transaction count is greater than 999"""

    def __init__(self, transaction_count):
        logging.error('Transaction limit reached: %s' % transaction_count)


class LogoutError(BetfairError):
    """Exception raised if status_code is not found"""

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API logout error, http error: %s' % response.status_code)
        else:
            logging.error('API logout %s: %s' % (response.get('status'), response.get('error')))


class ParameterError(BetfairError):
    """Exception raised if parameter is incorrect"""

    def __init__(self, api_method):
        logging.error('API method %s must have parameters' % api_method)


class SessionTokenError(BetfairError):
    """Exception raised if session_token is None"""

    def __init__(self):
        logging.error('APIClient must have session_token')
