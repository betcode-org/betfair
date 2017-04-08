

class BetfairError(Exception):
    """
    Base class for Betfair Errors.
    """
    pass


class PasswordError(BetfairError):
    """
    Exception raised if password is not found.
    """

    def __init__(self, username):
        message = 'Password not found in .bashprofile for %s, add or pass to APIClient' % username
        super(PasswordError, self).__init__(message)


class AppKeyError(BetfairError):
    """
    Exception raised if appkey is not found.
    """

    def __init__(self, username):
        message = 'AppKey not found in .bashprofile for %s, add or pass to APIClient' % username
        super(AppKeyError, self).__init__(message)


class CertsError(BetfairError):
    """
    Exception raised if certs folder is not found.
    """

    def __init__(self, path='/certs/'):
        message = 'Certificate folder not found in %s' % path
        super(CertsError, self).__init__(message)


class StatusCodeError(BetfairError):
    """
    Exception raised if status code is incorrect.
    """

    def __init__(self, status_code):
        message = 'Status code error: %s' % status_code
        super(StatusCodeError, self).__init__(message)


class LoginError(BetfairError):
    """
    Exception raised if sessionToken is not found.
    """

    def __init__(self, response):
        login_status = response.get('loginStatus', 'UNKNOWN')
        message = 'API login: %s' % login_status
        super(LoginError, self).__init__(message)


class KeepAliveError(BetfairError):
    """
    Exception raised if keep alive fails.
    """

    def __init__(self, response):
        keep_alive_status = response.get('status', 'UNKNOWN')
        keep_alive_error = response.get('error')
        message = 'API keepAlive %s: %s' % (keep_alive_status, keep_alive_error)
        super(KeepAliveError, self).__init__(message)


class APIError(BetfairError):
    """
    Exception raised if error is found.
    """

    def __init__(self, response, method=None, params=None, exception=None):
        if response:
            error_data = response.get('error')
            message = '%s \nParams: %s \nException: %s \nError: %s \nFull Response: %s' % (
                method, params, exception, error_data, response
            )
        else:
            message = '%s \nParams: %s \nException: %s' % (
                method, params, exception
            )
        super(APIError, self).__init__(message)


class LogoutError(BetfairError):
    """
    Exception raised if logout errors.
    """

    def __init__(self, response):
        logout_status = response.get('status', 'UNKNOWN')
        logout_error = response.get('error')
        message = 'API logout %s: %s' % (logout_status, logout_error)
        super(LogoutError, self).__init__(message)


# class ParameterError(BetfairError):
#     """Exception raised if parameter is incorrect"""
#
#     def __init__(self, api_method):
#         message = 'API method %s must have parameters' % api_method
#         super(ParameterError, self).__init__(message)
#
#
# class SessionTokenError(BetfairError):
#     """Exception raised if session_token is None"""
#
#     def __init__(self):
#         message = 'APIClient must have session_token'
#         super(SessionTokenError, self).__init__(message)


class SocketError(BetfairError):
    """
    Exception raised if error with socket.
    """

    def __init__(self, message):
        super(SocketError, self).__init__(message)


class RaceCardError(BetfairError):
    """
    Exception raised if error with race card request.
    """

    def __init__(self, message):
        super(RaceCardError, self).__init__(message)
