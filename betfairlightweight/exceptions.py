from typing import Union, Optional


class BetfairError(Exception):
    """
    Base class for Betfair Errors.
    """


class PasswordError(BetfairError):
    """
    Exception raised if password is not found.
    """

    def __init__(self, username: str):
        super().__init__(username)
        self.username = username

    def __str__(self):
        return f"Password not found in .bashprofile for {self.username}, add or pass to APIClient"


class AppKeyError(BetfairError):
    """
    Exception raised if appkey is not found.
    """

    def __init__(self, username: str):
        super().__init__(username)
        self.username = username

    def __str__(self):
        return f"AppKey not found in .bashprofile for {self.username}, add or pass to APIClient"


class CertsError(BetfairError):
    """
    Exception raised if certs not found.
    """


class StatusCodeError(BetfairError):
    """
    Exception raised if status code is incorrect.
    """

    def __init__(self, status_code: str):
        super().__init__(status_code)
        self.status_code = status_code

    def __str__(self):
        return f"Status code error: {self.status_code}"


class InvalidResponse(BetfairError):
    """
    Exception raised if invalid response
    received from betfair.
    """

    def __init__(self, response: Union[dict, list]):
        super().__init__(response)
        self.response = response

    def __str__(self):
        return f"Invalid response received: {self.response}"


class LoginError(BetfairError):
    """
    Exception raised if sessionToken is not found.
    """

    def __init__(self, response: dict):
        super().__init__(response)
        self.response = response

    def __str__(self):
        login_status = self.response.get("loginStatus")
        if login_status is None:  # different response when interactive login requested
            login_status = self.response.get("error", "UNKNOWN")
        return f"API login: {login_status}"


class KeepAliveError(BetfairError):
    """
    Exception raised if keep alive fails.
    """

    def __init__(self, response: dict):
        super().__init__(response)
        self.response = response

    def __str__(self):
        keep_alive_status = self.response.get("status", "UNKNOWN")
        keep_alive_error = self.response.get("error")
        return f"API keepAlive {keep_alive_status}: {keep_alive_error}"


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
        super().__init__(response, method, params, exception)
        self.response = response
        self.method = method
        self.params = params
        self.exception = exception

    def __str__(self):
        if not self.response:
            return (
                f"{self.method} \nParams: {self.params} \nException: {self.exception}"
            )
        error_data = self.response.get("error")
        return (
            f"{self.method} \nParams: {self.params} \nException: {self.exception} \n"
            f"Error: {error_data} \nFull Response: {self.response}"
        )


class LogoutError(BetfairError):
    """
    Exception raised if logout errors.
    """

    def __init__(self, response: dict):
        super().__init__(response)
        self.response = response

    def __str__(self):
        logout_status = self.response.get("status", "UNKNOWN")
        logout_error = self.response.get("error")
        return f"API logout {logout_status}: {logout_error}"


class SocketError(BetfairError):
    """
    Exception raised if error with socket.
    """


class ListenerError(BetfairError):
    """
    Exception raised if error with listener.
    """

    def __init__(self, connection_id: str, data: str):
        super().__init__(connection_id, data)
        self.connection_id = connection_id
        self.data = data

    def __str__(self):
        return f"connection_id: {self.connection_id}, data: {self.data}"


class CacheError(BetfairError):
    """
    Exception raised if error with cache.
    """


class RaceCardError(BetfairError):
    """
    Exception raised if error with race card request.
    """
