

class BetfairError(Exception):
    pass


class AppKeyError(BetfairError):
    pass


class LoginError(BetfairError):
    pass


class KeepAliveError(BetfairError):
    pass


class APIError(BetfairError):
    pass


class ParamsError(BetfairError):
    pass


class TransactionCountError(BetfairError):
    pass


class LogoutError(BetfairError):
    pass
