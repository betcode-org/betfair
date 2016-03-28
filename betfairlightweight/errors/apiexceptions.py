import logging
import betfairlightweight.errors.apierrors as apierrors


class BetfairError(Exception):
    pass


class AppKeyError(BetfairError):

    def __init__(self, username):
        logging.error('AppKey not found for %s' % username)


class LoginError(BetfairError):

    def __init__(self, response):
        login_status = response.get('loginStatus')
        description = apierrors.LOGIN_EXCEPTIONS[login_status]
        logging.error('API login %s: %s' % (login_status, description))


class KeepAliveError(BetfairError):

    def __init__(self, response):
        logging.error('API keepAlive %s: %s' % (response.get('status'), response.get('error')))


class APIError(BetfairError):
    pass


class TransactionCountError(BetfairError):

    def __init__(self, transaction_count):
        logging.error('Transaction limit reached: %s' % transaction_count)


class LogoutError(BetfairError):

    def __init__(self, response):
        logging.error('API logout %s: %s' % (response.get('status'), response.get('error')))
