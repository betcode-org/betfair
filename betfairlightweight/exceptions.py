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
        super(PasswordError, self).__init__(username)
        self.username = username

    def __str__(self):
        return (
            "Password not found in .bashprofile for %s, add or pass to APIClient"
            % self.username
        )


class AppKeyError(BetfairError):
    """
    Exception raised if appkey is not found.
    """

    def __init__(self, username: str):
        super(AppKeyError, self).__init__(username)
        self.username = username

    def __str__(self):
        return (
            "AppKey not found in .bashprofile for %s, add or pass to APIClient"
            % self.username
        )


class CertsError(BetfairError):
    """
    Exception raised if certs not found.
    """

    def __init__(self, message: str = None):
        super(CertsError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class StatusCodeError(BetfairError):
    """
    Exception raised if status code is incorrect.
    """

    def __init__(self, status_code: str):
        super(StatusCodeError, self).__init__(status_code)
        self.status_code = status_code

    def __str__(self):
        return "Status code error: %s" % self.status_code


class InvalidResponse(BetfairError):
    """
    Exception raised if invalid response
    received from betfair.
    """

    def __init__(self, response: Union[dict, list]):
        super(InvalidResponse, self).__init__(response)
        self.response = response

    def __str__(self):
        return "Invalid response received: %s" % self.response


class LoginError(BetfairError):
    """
    Exception raised if sessionToken is not found.
    """

    def __init__(self, response: dict):
        super(LoginError, self).__init__(response)
        self.response = response

    def __str__(self):
        login_status = self.response.get("loginStatus")
        if login_status is None:  # different response when interactive login requested
            login_status = self.response.get("error", "UNKNOWN")
        return "API login: %s" % login_status


class KeepAliveError(BetfairError):
    """
    Exception raised if keep alive fails.
    """

    def __init__(self, response: dict):
        super(KeepAliveError, self).__init__(response)
        self.response = response

    def __str__(self):
        keep_alive_status = self.response.get("status", "UNKNOWN")
        keep_alive_error = self.response.get("error")
        return "API keepAlive %s: %s" % (keep_alive_status, keep_alive_error)


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
        super(APIError, self).__init__(response, method, params, exception)
        self.response = response
        self.method = method
        self.params = params
        self.exception = exception

    def __str__(self):
        if self.response:
            error_data = self.response.get("error")
            return "%s \nParams: %s \nException: %s \nError: %s \nFull Response: %s" % (
                self.method,
                self.params,
                self.exception,
                error_data,
                self.response,
            )
        else:
            return "%s \nParams: %s \nException: %s" % (
                self.method,
                self.params,
                self.exception,
            )


class LogoutError(BetfairError):
    """
    Exception raised if logout errors.
    """

    def __init__(self, response: dict):
        super(LogoutError, self).__init__(response)
        self.response = response

    def __str__(self):
        logout_status = self.response.get("status", "UNKNOWN")
        logout_error = self.response.get("error")
        return "API logout %s: %s" % (logout_status, logout_error)


class SocketError(BetfairError):
    """
    Exception raised if error with socket.
    """

    def __init__(self, message: str):
        super(SocketError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ListenerError(BetfairError):
    """
    Exception raised if error with listener.
    """

    def __init__(self, connection_id: str, data: str):
        super(ListenerError, self).__init__(connection_id, data)
        self.connection_id = connection_id
        self.data = data

    def __str__(self):
        return "connection_id: %s, data: %s" % (self.connection_id, self.data)


class CacheError(BetfairError):
    """
    Exception raised if error with cache.
    """

    def __init__(self, message: str):
        super(CacheError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class RaceCardError(BetfairError):
    """
    Exception raised if error with race card request.
    """

    def __init__(self, message: str):
        super(RaceCardError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message
