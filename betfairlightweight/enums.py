from enum import Enum


GENERIC_JSON_RPC_EXCEPTIONS = {
    -32700: "Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.",
    -32601: "Method not found",
    -32602: "Problem parsing the parameters, or a mandatory parameter was not found",
    -32603: "Internal JSON-RPC error",
}


class RaceStatusEnum(Enum):
    DORMANT = "There is no data available for this race."
    DELAYED = "The start of the race has been delayed"
    PARADING = "The horses are in the parade ring"
    GOINGDOWN = "The horses are going down to the starting post"
    GOINGBEHIND = "The horses are going behind the stalls"
    ATTHEPOST = "The horses are at the post"
    UNDERORDERS = "The horses are loaded into the stalls/race is about to start"
    OFF = "The race has started"
    FINISHED = "The race has finished"
    FALSESTART = "There has been a false start"
    PHOTOGRAPH = "The result of the race is subject to a photo finish"
    RESULT = "The result of the race has been announced"
    WEIGHEDIN = "The jockeys have weighed in"
    RACEVOID = "The race has been declared void"
    ABANDONED = "The meeting has been cancelled"


class LoginExceptions(Enum):
    INVALID_USERNAME_OR_PASSWORD = "The username or password are invalid"
    ACCOUNT_NOW_LOCKED = "The account was just locked"
    ACCOUNT_ALREADY_LOCKED = "The account is already locked"
    PENDING_AUTH = "Pending authentication"
    TELBET_TERMS_CONDITIONS_NA = "Telbet terms and conditions rejected"
    DUPLICATE_CARDS = "Duplicate cards"
    SECURITY_QUESTION_WRONG_3X = (
        "The user has entered wrong the security answer 3 times"
    )
    KYC_SUSPEND = "KYC suspended"
    SUSPENDED = "The account is suspended"
    CLOSED = "The account is closed"
    SELF_EXCLUDED = "The account has been self-excluded"
    INVALID_CONNECTIVITY_TO_REGULATOR_DK = (
        "The DK regulator cannot be accessed due to some internal problems in the "
        "system behind or in at regulator; timeout cases included."
    )
    NOT_AUTHORIZED_BY_REGULATOR_DK = (
        "The user identified by the given credentials is not authorized in the DKs "
        "jurisdictions due to the regulators policies. Ex = the user for which "
        "this session should be created is not allowed to act(play bet) in the DKs "
        "jurisdiction."
    )
    INVALID_CONNECTIVITY_TO_REGULATOR_IT = (
        "The IT regulator cannot be accessed due to some internal problems in the "
        "system behind or in at regulator; timeout cases included."
    )
    NOT_AUTHORIZED_BY_REGULATOR_IT = (
        "The user identified by the given credentials is not authorized in the ITs "
        "jurisdictions due to the regulators policies. Ex = the user for which this "
        "session should be created is not allowed to act(play bet) in the ITs "
        "jurisdiction."
    )
    SECURITY_RESTRICTED_LOCATION = "The account is restricted due to security concerns"
    BETTING_RESTRICTED_LOCATION = (
        "The account is accessed from a location where betting is restricted"
    )
    TRADING_MASTER = "Trading Master Account"
    TRADING_MASTER_SUSPENDED = "Suspended Trading Master Account"
    AGENT_CLIENT_MASTER = "Agent Client Master"
    AGENT_CLIENT_MASTER_SUSPENDED = "Suspended Agent Client Master"
    DANISH_AUTHORIZATION_REQUIRED = "Danish authorization required"
    SPAIN_MIGRATION_REQUIRED = "Spain migration required"
    DENMARK_MIGRATION_REQUIRED = "Denmark migration required"
    SPANISH_TERMS_ACCEPTANCE_REQUIRED = (
        "The latest Spanish terms and conditions version must be accepted"
    )
    ITALIAN_CONTRACT_ACCEPTANCE_REQUIRED = (
        "The latest Italian contract version must be accepted"
    )
    CERT_AUTH_REQUIRED = (
        "Certificate required or certificate present but could not authenticate with it"
    )
    CHANGE_PASSWORD_REQUIRED = "Change password required"
    PERSONAL_MESSAGE_REQUIRED = "Personal message required for the user"
    INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRE = (
        "The latest international terms and conditions must be accepted prior "
        "to logging in."
    )
    EMAIL_LOGIN_NOT_ALLOWED = "This account has not opted in to log in with the email"
    MULTIPLE_USERS_WITH_SAME_CREDENTIAL = (
        "There is more than one account with the same credential"
    )
    ACCOUNT_PENDING_PASSWORD_CHANGE = (
        "The account must undergo password recovery to reactivate"
    )
    TEMPORARY_BAN_TOO_MANY_REQUEST = (
        "The limit for successful login requests per minute has been exceeded. New "
        "login attempts will be banned for 20 minutes"
    )


class ApingException(Enum):
    TOO_MUCH_DATA = "The operation requested too much data exceeding the Market Data Request Limits."
    INVALID_INPUT_DATA = (
        "The data input is invalid. A specific description is returned via errorDetails as shown "
        "below."
    )
    INVALID_SESSION_INFORMATION = (
        "The session token hasnt been provided is invalid or has expired."
    )
    NO_APP_KEY = (
        "An application key header (X-Application) has not been provided in the request"
    )
    NO_SESSION = (
        "A session token header (X-Authentication) has not been provided in the request"
    )
    UNEXPECTED_ERROR = "An unexpected internal error occurred that prevented successful request processing."
    INVALID_APP_KEY = "The application key passed is invalid or is not present"
    TOO_MANY_REQUESTS = (
        "There are too many pending requests e.g. a listMarketBook with Order/Match projections is "
        "limited to 3 concurrent requests. The error also applies to listCurrentOrders "
        "listMarketProfitAndLoss and listClearedOrders if you have 3 or more requests currently "
        "in execution"
    )
    SERVICE_BUSY = "The service is currently too busy to service this request."
    TIMEOUT_ERROR = (
        "The Internal call to downstream service timed out. Please note = If a TIMEOUT_ERROR error "
        "occurs on a placeOrders/replaceOrders request you should check listCurrentOrders to verify the "
        "status of your bets before placing further orders. Please allow up to 2 minutes for timed out "
        "order to appear."
    )
    REQUEST_SIZE_EXCEEDS_LIMIT = (
        "The request exceeds the request size limit. Requests are limited to a total of 250 "
        "betId's/marketId's (or a combination of both)."
    )
    ACCESS_DENIED = (
        "The calling client is not permitted to perform the specific action e.g. the using a Delayed "
        "App Key when placing bets or attempting to place a bet from a restricted jurisdiction."
    )


class MarketStatus(Enum):
    INACTIVE = "The market has been created but isn't yet available."
    OPEN = "The market is open for betting."
    SUSPENDED = "The market is suspended and not available for betting."
    CLOSED = "The market has been settled and is no longer available for betting."


class InstructionReportStatus(Enum):
    SUCCESS = ""
    FAILURE = ""
    TIMEOUT = ""


class InstructionReportErrorCode(Enum):
    INVALID_BET_SIZE = "bet size is invalid for your currency or your regulator"
    INVALID_RUNNER = "Runner does not exist includes vacant traps in greyhound racing"
    BET_TAKEN_OR_LAPSED = (
        "Bet cannot be cancelled or modified as it has already been taken or has lapsed Includes "
        "attempts to cancel/modify market on close BSP bets and cancelling limit on close BSP bets"
    )
    BET_IN_PROGRESS = (
        "No result was received from the matcher in a timeout configured for the system"
    )
    RUNNER_REMOVED = "Runner has been removed from the event"
    MARKET_NOT_OPEN_FOR_BETTING = "Attempt to edit a bet on a market that has closed."
    LOSS_LIMIT_EXCEEDED = (
        "The action has caused the account to exceed the self imposed loss limit"
    )
    MARKET_NOT_OPEN_FOR_BSP_BETTING = (
        "Market now closed to bsp betting. Turned in-play or has been reconciled"
    )
    INVALID_PRICE_EDIT = (
        "Attempt to edit down the price of a bsp limit on close lay bet or edit up the price of a "
        "limit on close back bet"
    )
    INVALID_ODDS = "Odds not on price ladder - either edit or placement"
    INSUFFICIENT_FUNDS = (
        "Insufficient funds available to cover the bet action. Either the exposure limit or "
        "available to bet limit would be exceeded"
    )
    INVALID_PERSISTENCE_TYPE = (
        "Invalid persistence type for this market e.g. KEEP for a non bsp market"
    )
    ERROR_IN_MATCHER = (
        "A problem with the matcher prevented this action completing successfully"
    )
    INVALID_BACK_LAY_COMBINATION = (
        "The order contains a back and a lay for the same runner at overlapping prices. "
        "This would guarantee a self match. This also applies to BSP limit on close bets"
    )
    ERROR_IN_ORDER = "The action failed because the parent order failed"
    INVALID_BID_TYPE = "Bid type is mandatory"
    INVALID_BET_ID = "Bet for id supplied has not been found"
    CANCELLED_NOT_PLACED = "Bet cancelled but replacement bet was not placed"
    RELATED_ACTION_FAILED = (
        "Action failed due to the failure of a action on which this action is dependent"
    )
    NO_ACTION_REQUIRED = (
        "the action does not result in any state change. eg changing a persistence to it's "
        "current value"
    )


class ExecutionReportStatus(Enum):
    SUCCESS = "Order processed successfully"
    FAILURE = "Order failed."
    PROCESSED_WITH_ERRORS = (
        "The order itself has been accepted but at least one (possibly all) actions have "
        "generated errors. This error only occurs for replaceOrders cancelOrders and "
        "updateOrders operations. The placeOrders operation will not return "
        "PROCESSED_WITH_ERRORS status as it is an atomic operation."
    )
    TIMEOUT = "Order timed out."


class ExecutionReportErrorCode(Enum):
    ERROR_IN_MATCHER = "The matcher is not healthy"
    PROCESSED_WITH_ERRORS = (
        "The order itself has been accepted but at least one (possibly all) actions have "
        "generated errors"
    )
    BET_ACTION_ERROR = (
        "There is an error with an action that has caused the entire order to be rejected. Check "
        "the instructionReports errorCode for the reason for the rejection of the order."
    )
    INVALID_ACCOUNT_STATE = (
        "Order rejected due to the account's status (suspended inactive dup cards)"
    )
    INVALID_WALLET_STATUS = "Order rejected due to the account's wallet's status"
    INSUFFICIENT_FUNDS = (
        "Account has exceeded its exposure limit or available to bet limit"
    )
    LOSS_LIMIT_EXCEEDED = "The account has exceed the self imposed loss limit"
    MARKET_SUSPENDED = "Market is suspended"
    MARKET_NOT_OPEN_FOR_BETTING = (
        "Market is not open for betting. It is either not yet active suspended or closed "
        "awaiting settlement."
    )
    DUPLICATE_TRANSACTION = (
        "Duplicate customer reference data submitted - Please note: There is a time window "
        "associated with the de-duplication of duplicate submissions which is 60 second"
    )
    INVALID_ORDER = (
        "Order cannot be accepted by the matcher due to the combination of actions. For example bets "
        "being edited are not on the same market or order includes both edits and placement"
    )
    INVALID_MARKET_ID = "Market doesn't exist"
    PERMISSION_DENIED = (
        "Business rules do not allow order to be placed. You are either attempting to place the "
        "order using a Delayed Application Key or from a restricted jurisdiction (i.e. USA)"
    )
    DUPLICATE_BETIDS = "duplicate bet ids found"
    NO_ACTION_REQUIRED = "Order hasn't been passed to matcher as system detected there will be no state change"
    SERVICE_UNAVAILABLE = "The requested service is unavailable"
    REJECTED_BY_REGULATOR = (
        "The regulator rejected the order. On the Italian Exchange this error will occur if "
        "more than 50 bets are sent in a single placeOrders request."
    )


class StreamingProtocolErrors(Enum):
    """General errors not sent with id linking to specific request (as no request context)"""

    INVALID_INPUT = "Failure code returned when an invalid input is provided (could not deserialize the message)"
    TIMEOUT = "Failure code when a client times out (i.e. too slow sending data)"


class StreamingAuthenticationErrors(Enum):
    """Specific to authentication"""

    NO_APP_KEY = (
        "Failure code returned when an application key is not found in the message"
    )
    INVALID_APP_KEY = (
        "Failure code returned when an invalid application key is received"
    )
    NO_SESSION = (
        "Failure code returned when a session token is not found in the message"
    )
    INVALID_SESSION_INFORMATION = (
        "Failure code returned when an invalid session token is received"
    )
    NOT_AUTHORIZED = (
        "Failure code returned when client is not authorized to perform the operation"
    )
    MAX_CONNECTION_LIMIT_EXCEEDED = (
        "Failure code returned when a client tries to create more connections than "
        "allowed to"
    )


class StreamingSubscriptionErrors(Enum):
    """Specific to subscription requests"""

    SUBSCRIPTION_LIMIT_EXCEEDED = (
        "Customer tried to subscribe to more markets than allowed to"
    )
    INVALID_CLOCK = (
        "Failure code returned when an invalid clock is provided on re-subscription (check initialClk / "
        "clk supplied)"
    )


class StreamingGeneralErrors(Enum):
    """General errors which may or may not be linked to specific request id"""

    UNEXPECTED_ERROR = (
        "Failure code returned when an internal error occurred on the server"
    )
    CONNECTION_FAILED = (
        "Failure code used when the client / server connection is terminated"
    )


class StreamingSide(Enum):
    """Some enums are provided in shorthand"""

    L = "LAY"
    B = "BACK"


class StreamingStatus(Enum):
    E = "EXECUTABLE"
    EC = "EXECUTION_COMPLETE"


class StreamingPersistenceType(Enum):
    L = "LAPSE"
    P = "PERSIST"
    MOC = "MARKET_ON_CLOSE"


class StreamingOrderType(Enum):
    L = "LIMIT"
    MOC = "MARKET_ON_CLOSE"
    LOC = "LIMIT_ON_CLOSE"


class StreamingRegulatorCode(Enum):
    REG_GGC = "GIBRALTAR REGULATOR"
