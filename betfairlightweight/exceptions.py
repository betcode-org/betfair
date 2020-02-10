from typing import Union, Optional


class BetfairError(Exception):
    """
    Base class for Betfair Errors.
    """

    pass


class PasswordError(BetfairError):
    """
    Exception raised if password is not found.
    """

    def __init__(self, username: str):
        message = (
            "Password not found in .bashprofile for %s, add or pass to APIClient"
            % username
        )
        super(PasswordError, self).__init__(message)


class AppKeyError(BetfairError):
    """
    Exception raised if appkey is not found.
    """

    def __init__(self, username: str):
        message = (
            "AppKey not found in .bashprofile for %s, add or pass to APIClient"
            % username
        )
        super(AppKeyError, self).__init__(message)


class CertsError(BetfairError):
    """
    Exception raised if certs not found.
    """

    def __init__(self, message: str = None):
        super(CertsError, self).__init__(message)


class StatusCodeError(BetfairError):
    """
    Exception raised if status code is incorrect.
    """

    def __init__(self, status_code: str):
        message = "Status code error: %s" % status_code
        super(StatusCodeError, self).__init__(message)


class InvalidResponse(BetfairError):
    """
    Exception raised if invalid response
    received from betfair.
    """

    def __init__(self, response: Union[dict, list]):
        message = "Invalid response received: %s" % response
        super(InvalidResponse, self).__init__(message)


class LoginError(BetfairError):
    """
    Exception raised if sessionToken is not found.
    """

    def __init__(self, response: dict):
        login_status = response.get("loginStatus")
        if login_status is None:  # different response when interactive login requested
            login_status = response.get("error", "UNKNOWN")
        message = "API login: %s" % login_status
        super(LoginError, self).__init__(message)


class KeepAliveError(BetfairError):
    """
    Exception raised if keep alive fails.
    """

    def __init__(self, response: dict):
        keep_alive_status = response.get("status", "UNKNOWN")
        keep_alive_error = response.get("error")
        message = "API keepAlive %s: %s" % (keep_alive_status, keep_alive_error)
        super(KeepAliveError, self).__init__(message)


class APIError(BetfairError):
    """
    Exception raised if error is found.
    """

    def __init__(
        self,
        response: Optional[dict],
        method: str = None,
        params: dict = None,
        exception: Exception = None,
    ):
        if response:
            error_data = response.get("error")
            message = (
                "%s \nParams: %s \nException: %s \nError: %s \nFull Response: %s"
                % (method, params, exception, error_data, response)
            )
        else:
            message = "%s \nParams: %s \nException: %s" % (method, params, exception)
        super(APIError, self).__init__(message)


class LogoutError(BetfairError):
    """
    Exception raised if logout errors.
    """

    def __init__(self, response: dict):
        logout_status = response.get("status", "UNKNOWN")
        logout_error = response.get("error")
        message = "API logout %s: %s" % (logout_status, logout_error)
        super(LogoutError, self).__init__(message)


class SocketError(BetfairError):
    """
    Exception raised if error with socket.
    """

    def __init__(self, message: str):
        super(SocketError, self).__init__(message)


class ListenerError(BetfairError):
    """
    Exception raised if error with listener.
    """

    def __init__(self, connection_id: str, data: str):
        message = "connection_id: %s, data: %s" % (connection_id, data)
        super(ListenerError, self).__init__(message)


class CacheError(BetfairError):
    """
    Exception raised if error with cache.
    """

    def __init__(self, message: str):
        super(CacheError, self).__init__(message)


class RaceCardError(BetfairError):
    """
    Exception raised if error with race card request.
    """

    def __init__(self, message: str):
        super(RaceCardError, self).__init__(message)
