import logging
import betfairlightweight.errors.apierrors as apierrors


class BetfairError(Exception):
    pass


class AppKeyError(BetfairError):

    def __init__(self, username):
        logging.error('AppKey not found for %s' % username)


class LoginError(BetfairError):

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API login error, http error: %s' % response.status_code)
        else:
            login_status = response.get('loginStatus')
            description = apierrors.LOGIN_EXCEPTIONS[login_status]
            logging.error('API login %s: %s' % (login_status, description))


class KeepAliveError(BetfairError):

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API keepAlive error, http error: %s' % response.status_code)
        else:
            logging.error('API keepAlive %s: %s' % (response.get('status'), response.get('error')))


class APIError(BetfairError):

    def __init__(self, response, params, method=None, exception=None):
        if response is not None:
            if hasattr(response, 'status_code') and response.status_code != 200:
                logging.error('APIError, http error: %s' % response.status_code)
            else:
                code = response['error']['code']
                description = apierrors.GENERIC_JSON_RPC_EXCEPTIONS.get(code)
                error_details = None
                if not description:
                    error_code = response['error']['data']['APINGException']['errorCode']
                    error_details = response['error']['data']['APINGException']['errorDetails']
                    description = apierrors.APING_EXCEPTION.get(error_code)
                logging.error('API betting %s: %s' % (code, description))
                logging.error('Method: %s, Parameters sent: %s' % (method, params))
                logging.error('Error details: %s' % error_details)
        else:
            logging.error('APIError error: %s' % exception)


class TransactionCountError(BetfairError):

    def __init__(self, transaction_count):
        logging.error('Transaction limit reached: %s' % transaction_count)


class LogoutError(BetfairError):

    def __init__(self, response):
        if hasattr(response, 'status_code') and response.status_code != 200:
            logging.error('API logout error, http error: %s' % response.status_code)
        else:
            logging.error('API logout %s: %s' % (response.get('status'), response.get('error')))
