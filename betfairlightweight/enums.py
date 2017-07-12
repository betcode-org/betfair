from enum import Enum


GENERIC_JSON_RPC_EXCEPTIONS = {
    -32700: 'Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.',
    -32601: 'Method not found',
    -32602: 'Problem parsing the parameters, or a mandatory parameter was not found',
    -32603: 'Internal JSON-RPC error'
}


class RaceStatusEnum(Enum):
    DORMANT = 'There is no data available for this race.'
    DELAYED = 'The start of the race has been delayed'
    PARADING = 'The horses are in the parade ring'
    GOINGDOWN = 'The horses are going down to the starting post'
    GOINGBEHIND = 'The horses are going behind the stalls'
    ATTHEPOST = 'The horses are at the post'
    UNDERORDERS = 'The horses are loaded into the stalls/race is about to start'
    OFF = 'The race has started'
    FINISHED = 'The race has finished'
    FALSESTART = 'There has been a false start'
    PHOTOGRAPH = 'The result of the race is subject to a photo finish'
    RESULT = 'The result of the race has been announced'
    WEIGHEDIN = 'The jockeys have weighed in'
    RACEVOID = 'The race has been declared void'
    ABANDONED = 'The meeting has been cancelled'


class LoginExceptions(Enum):
    INVALID_USERNAME_OR_PASSWORD = "The username or password are invalid"
    ACCOUNT_NOW_LOCKED = "The account was just locked"
    ACCOUNT_ALREADY_LOCKED = "The account is already locked"
    PENDING_AUTH = "Pending authentication"
    TELBET_TERMS_CONDITIONS_NA = "Telbet terms and conditions rejected"
    DUPLICATE_CARDS = "Duplicate cards"
    SECURITY_QUESTION_WRONG_3X = "The user has entered wrong the security answer 3 times"
    KYC_SUSPEND = "KYC suspended"
    SUSPENDED = "The account is suspended"
    CLOSED = "The account is closed"
    SELF_EXCLUDED = "The account has been self-excluded"
    INVALID_CONNECTIVITY_TO_REGULATOR_DK = "The DK regulator cannot be accessed due to some internal problems in the " \
                                           "system behind or in at regulator; timeout cases included."
    NOT_AUTHORIZED_BY_REGULATOR_DK = "The user identified by the given credentials is not authorized in the DKs " \
                                     "jurisdictions due to the regulators policies. Ex = the user for which " \
                                     "this session should be created is not allowed to act(play bet) in the DKs " \
                                     "jurisdiction."
    INVALID_CONNECTIVITY_TO_REGULATOR_IT = "The IT regulator cannot be accessed due to some internal problems in the " \
                                           "system behind or in at regulator; timeout cases included."
    NOT_AUTHORIZED_BY_REGULATOR_IT = "The user identified by the given credentials is not authorized in the ITs " \
                                     "jurisdictions due to the regulators policies. Ex = the user for which this " \
                                     "session should be created is not allowed to act(play bet) in the ITs " \
                                     "jurisdiction."
    SECURITY_RESTRICTED_LOCATION = "The account is restricted due to security concerns"
    BETTING_RESTRICTED_LOCATION = "The account is accessed from a location where betting is restricted"
    TRADING_MASTER = "Trading Master Account"
    TRADING_MASTER_SUSPENDED = "Suspended Trading Master Account"
    AGENT_CLIENT_MASTER = "Agent Client Master"
    AGENT_CLIENT_MASTER_SUSPENDED = "Suspended Agent Client Master"
    DANISH_AUTHORIZATION_REQUIRED = "Danish authorization required"
    SPAIN_MIGRATION_REQUIRED = "Spain migration required"
    DENMARK_MIGRATION_REQUIRED = "Denmark migration required"
    SPANISH_TERMS_ACCEPTANCE_REQUIRED = "The latest Spanish terms and conditions version must be accepted"
    ITALIAN_CONTRACT_ACCEPTANCE_REQUIRED = "The latest Italian contract version must be accepted"
    CERT_AUTH_REQUIRED = "Certificate required or certificate present but could not authenticate with it"
    CHANGE_PASSWORD_REQUIRED = "Change password required"
    PERSONAL_MESSAGE_REQUIRED = "Personal message required for the user"
    INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRE = "The latest international terms and conditions must be accepted prior " \
                                             "to logging in."
    EMAIL_LOGIN_NOT_ALLOWED = "This account has not opted in to log in with the email"
    MULTIPLE_USERS_WITH_SAME_CREDENTIAL = "There is more than one account with the same credential"
    ACCOUNT_PENDING_PASSWORD_CHANGE = "The account must undergo password recovery to reactivate"
    TEMPORARY_BAN_TOO_MANY_REQUEST = "The limit for successful login requests per minute has been exceeded. New " \
                                     "login attempts will be banned for 20 minutes"


class ApingException(Enum):
    TOO_MUCH_DATA = "The operation requested too much data exceeding the Market Data Request Limits."
    INVALID_INPUT_DATA = "The data input is invalid. A specific description is returned via errorDetails as shown " \
                         "below."
    INVALID_SESSION_INFORMATION = "The session token hasnt been provided is invalid or has expired."
    NO_APP_KEY = "An application key header (X-Application) has not been provided in the request"
    NO_SESSION = "A session token header (X-Authentication) has not been provided in the request"
    UNEXPECTED_ERROR = "An unexpected internal error occurred that prevented successful request processing."
    INVALID_APP_KEY = "The application key passed is invalid or is not present"
    TOO_MANY_REQUESTS = "There are too many pending requests e.g. a listMarketBook with Order/Match projections is " \
                        "limited to 3 concurrent requests. The error also applies to listCurrentOrders " \
                        "listMarketProfitAndLoss and listClearedOrders if you have 3 or more requests currently " \
                        "in execution"
    SERVICE_BUSY = "The service is currently too busy to service this request."
    TIMEOUT_ERROR = "The Internal call to downstream service timed out. Please note = If a TIMEOUT_ERROR error " \
                    "occurs on a placeOrders/replaceOrders request you should check listCurrentOrders to verify the " \
                    "status of your bets before placing further orders. Please allow up to 2 minutes for timed out " \
                    "order to appear."
    REQUEST_SIZE_EXCEEDS_LIMIT = "The request exceeds the request size limit. Requests are limited to a total of 250 " \
                                 "betId's/marketId's (or a combination of both)."
    ACCESS_DENIED = "The calling client is not permitted to perform the specific action e.g. the using a Delayed " \
                    "App Key when placing bets or attempting to place a bet from a restricted jurisdiction."


class MarketStatus(Enum):
    INACTIVE = "The market has been created but isn't yet available."
    OPEN = "The market is open for betting."
    SUSPENDED = "The market is suspended and not available for betting."
    CLOSED = "The market has been settled and is no longer available for betting."


class InstructionReportStatus(Enum):
    SUCCESS = ''
    FAILURE = ''
    TIMEOUT = ''


class InstructionReportErrorCode(Enum):
    INVALID_BET_SIZE = "bet size is invalid for your currency or your regulator"
    INVALID_RUNNER = "Runner does not exist includes vacant traps in greyhound racing"
    BET_TAKEN_OR_LAPSED = "Bet cannot be cancelled or modified as it has already been taken or has lapsed Includes " \
                          "attempts to cancel/modify market on close BSP bets and cancelling limit on close BSP bets"
    BET_IN_PROGRESS = "No result was received from the matcher in a timeout configured for the system"
    RUNNER_REMOVED = "Runner has been removed from the event"
    MARKET_NOT_OPEN_FOR_BETTING = "Attempt to edit a bet on a market that has closed."
    LOSS_LIMIT_EXCEEDED = "The action has caused the account to exceed the self imposed loss limit"
    MARKET_NOT_OPEN_FOR_BSP_BETTING = "Market now closed to bsp betting. Turned in-play or has been reconciled"
    INVALID_PRICE_EDIT = "Attempt to edit down the price of a bsp limit on close lay bet or edit up the price of a " \
                         "limit on close back bet"
    INVALID_ODDS = "Odds not on price ladder - either edit or placement"
    INSUFFICIENT_FUNDS = "Insufficient funds available to cover the bet action. Either the exposure limit or " \
                         "available to bet limit would be exceeded"
    INVALID_PERSISTENCE_TYPE = "Invalid persistence type for this market e.g. KEEP for a non bsp market"
    ERROR_IN_MATCHER = "A problem with the matcher prevented this action completing successfully"
    INVALID_BACK_LAY_COMBINATION = "The order contains a back and a lay for the same runner at overlapping prices. " \
                                   "This would guarantee a self match. This also applies to BSP limit on close bets"
    ERROR_IN_ORDER = "The action failed because the parent order failed"
    INVALID_BID_TYPE = "Bid type is mandatory"
    INVALID_BET_ID = "Bet for id supplied has not been found"
    CANCELLED_NOT_PLACED = "Bet cancelled but replacement bet was not placed"
    RELATED_ACTION_FAILED = "Action failed due to the failure of a action on which this action is dependent"
    NO_ACTION_REQUIRED = "the action does not result in any state change. eg changing a persistence to it's " \
                         "current value"


class ExecutionReportStatus(Enum):
    SUCCESS = "Order processed successfully"
    FAILURE = "Order failed."
    PROCESSED_WITH_ERRORS = "The order itself has been accepted but at least one (possibly all) actions have " \
                            "generated errors. This error only occurs for replaceOrders cancelOrders and " \
                            "updateOrders operations. The placeOrders operation will not return " \
                            "PROCESSED_WITH_ERRORS status as it is an atomic operation."
    TIMEOUT = "Order timed out."


class ExecutionReportErrorCode(Enum):
    ERROR_IN_MATCHER = "The matcher is not healthy"
    PROCESSED_WITH_ERRORS = "The order itself has been accepted but at least one (possibly all) actions have " \
                            "generated errors"
    BET_ACTION_ERROR = "There is an error with an action that has caused the entire order to be rejected. Check " \
                       "the instructionReports errorCode for the reason for the rejection of the order."
    INVALID_ACCOUNT_STATE = "Order rejected due to the account's status (suspended inactive dup cards)"
    INVALID_WALLET_STATUS = "Order rejected due to the account's wallet's status"
    INSUFFICIENT_FUNDS = "Account has exceeded its exposure limit or available to bet limit"
    LOSS_LIMIT_EXCEEDED = "The account has exceed the self imposed loss limit"
    MARKET_SUSPENDED = "Market is suspended"
    MARKET_NOT_OPEN_FOR_BETTING = "Market is not open for betting. It is either not yet active suspended or closed " \
                                  "awaiting settlement."
    DUPLICATE_TRANSACTION = "Duplicate customer reference data submitted - Please note: There is a time window " \
                            "associated with the de-duplication of duplicate submissions which is 60 second"
    INVALID_ORDER = "Order cannot be accepted by the matcher due to the combination of actions. For example bets " \
                    "being edited are not on the same market or order includes both edits and placement"
    INVALID_MARKET_ID = "Market doesn't exist"
    PERMISSION_DENIED = "Business rules do not allow order to be placed. You are either attempting to place the " \
                        "order using a Delayed Application Key or from a restricted jurisdiction (i.e. USA)"
    DUPLICATE_BETIDS = "duplicate bet ids found"
    NO_ACTION_REQUIRED = "Order hasn't been passed to matcher as system detected there will be no state change"
    SERVICE_UNAVAILABLE = "The requested service is unavailable"
    REJECTED_BY_REGULATOR = "The regulator rejected the order. On the Italian Exchange this error will occur if " \
                            "more than 50 bets are sent in a single placeOrders request."


class StreamingProtocolErrors(Enum):
    """General errors not sent with id linking to specific request (as no request context)
    """
    INVALID_INPUT = 'Failure code returned when an invalid input is provided (could not deserialize the message)'
    TIMEOUT = 'Failure code when a client times out (i.e. too slow sending data)'


class StreamingAuthenticationErrors(Enum):
    """Specific to authentication
    """
    NO_APP_KEY = 'Failure code returned when an application key is not found in the message'
    INVALID_APP_KEY = 'Failure code returned when an invalid application key is received'
    NO_SESSION = 'Failure code returned when a session token is not found in the message'
    INVALID_SESSION_INFORMATION = 'Failure code returned when an invalid session token is received'
    NOT_AUTHORIZED = 'Failure code returned when client is not authorized to perform the operation'
    MAX_CONNECTION_LIMIT_EXCEEDED = 'Failure code returned when a client tries to create more connections than ' \
                                    'allowed to'


class StreamingSubscriptionErrors(Enum):
    """Specific to subscription requests
    """
    SUBSCRIPTION_LIMIT_EXCEEDED = 'Customer tried to subscribe to more markets than allowed to'
    INVALID_CLOCK = 'Failure code returned when an invalid clock is provided on re-subscription (check initialClk / ' \
                    'clk supplied)'


class StreamingGeneralErrors(Enum):
    """General errors which may or may not be linked to specific request id
    """
    UNEXPECTED_ERROR = 'Failure code returned when an internal error occurred on the server'
    CONNECTION_FAILED = 'Failure code used when the client / server connection is terminated'


class StreamingSide(Enum):
    """Some enums are provided in shorthand
    """
    L = 'LAY'
    B = 'BACK'


class StreamingStatus(Enum):
    E = 'EXECUTABLE'
    EC = 'EXECUTION_COMPLETE'


class StreamingPersistenceType(Enum):
    L = 'LAPSE'
    P = 'PERSIST'
    MOC = 'MARKET_ON_CLOSE'


class StreamingOrderType(Enum):
    L = 'LIMIT'
    MOC = 'MARKET_ON_CLOSE'
    LOC = 'LIMIT_ON_CLOSE'


class StreamingRegulatorCode(Enum):
    REG_GGC = 'GIBRALTAR REGULATOR'


class MarketSort(Enum):
    """
    Specify how to sort market data received from Betfair APING.
    :var MINIMUM_TRADED: Minimum traded volume
    :var MAXIMUM_TRADED: Maximum traded volume
    :var MINIMUM_AVAILABLE: Minimum available to match
    :var MAXIMUM_AVAILABLE: Maximum available to match
    :var FIRST_TO_START: The closest markets based on their expected start time
    :var LAST_TO_START: The most distant markets based on their expected start time
    """
    MinTraded = 'MINIMUM_TRADED'
    maxTraded = 'MAXIMUM_TRADED'
    MinAvail = 'MINIMUM_AVAILABLE'
    MaxAvail = 'MAXIMUM_AVAILABLE'
    FirstStart = 'FIRST_TO_START'
    LatestStart = 'LAST_TO_START'


class MatchProjection(Enum):
    """
    How to aggregate orders.
    :var NO_ROLLUP: No rollup, return raw fragments
    :var ROLLED_UP_BY_PRICE: Rollup matched amounts by distinct matched prices per side.
    :var ROLLED_UP_BY_AVG_PRICE: Rollup matched amounts by average matched price per side
    """
    NoRoll = 'NO_ROLLUP'
    PriceRoll = 'ROLLED_UP_BY_PRICE'
    AvgPriceRoll = 'ROLLED_UP_BY_AVG_PRICE'


class OrderProjection(Enum):
    """
    Orders to include it market book data retrieved from exchange.
    :var ALL: EXECUTABLE and EXECUTION_COMPLETE orders
    :var EXECUTABLE: An order that has a remaining unmatched portion
    :var EXECUTION_COMPLETE: An order that does not have any remaining unmatched portion
    """
    All = 'ALL'
    Executable = 'EXECUTABLE'
    Traded = 'EXECUTION_COMPLETE'


class RunnerStatus(Enum):
    """
    :var ACTIVE: ACTIVE
    :var WINNER: WINNER
    :var LOSER: LOSER
    :var PLACED: The runner was placed, applies to EACH_WAY marketTypes only.
    :var REMOVED VACANT: REMOVED_VACANT applies to Greyhounds.
    :var REMOVED: REMOVED
    :var HIDDEN: The selection is hidden from the market. This occurs in Horse Racing markets if runner does not hold an official entry.
    """
    Active = 'ACTIVE'
    Winner = 'WINNER'
    Loser = 'LOSER'
    Vacant = 'REMOVED_VACANT'
    Removed = 'REMOVED'
    Hidden = 'HIDDEN'


class TimeGranularity(Enum):
    Days = 'DAYS'
    Hours = 'HOURS'
    Mins = 'MINUTES'


class Side(Enum):
    """
    Bet side
    :var BACK: To back a team, horse or outcome is to bet on the selection to win.
    :var LAY: To lay a team, horse, or outcome is to bet on the selection to lose.
    """
    Back = 'BACK'
    Lay = 'LAY'


class RollUpModel(Enum):
    """
    Roll up methods to apply to orders.
    :var STAKE: The volumes will be rolled up to the minimum value which is >= rollupLimit.
    :var PAYOUT: The volumes will be rolled up to the minimum value where the payout( price * volume ) is >= rollupLimit.
    :var MANAGED_LIABILITY: The volumes will be rolled up to the minimum value which is >= rollupLimit, until a lay price threshold.
                            There after, the volumes will be rolled up to the minimum value such that the liability >= a minimum liability.
    :var NONE: No rollup will be applied. However the volumes will be filtered by currency specific minimum stake unless overridden specifically for the channel.
    """
    Stake = 'STAKE'
    Payout = 'PAYOUT'
    Liability = 'MANAGED_LIABILITY'
    NoRoll = 'NONE'


class OrderBy(Enum):
    """
    Sort method to be applied to orders.
    :var BY_BET: Deprecated Use BY_PLACE_TIME instead. Order by placed time, then bet id.
    :var BY_MARKET: Order by market id, then placed time, then bet id.
    :var BY_MATCH_TIME: Order by time of last matched fragment (if any), then placed time, then bet id.
                        Filters out orders which have no matched date.
                        The dateRange filter (if specified) is applied to the matched date.
    :var BY_PLACE_TIME: Order by placed time, then bet id. This is an alias of to be deprecated BY_BET.
                        The dateRange filter (if specified) is applied to the placed date.
    :var BY_SETTLED_TIME: Order by time of last settled fragment (if any due to partial market settlement),
                          then by last match time, then placed time, then bet id.
                          Filters out orders which have not been settled.
                          The dateRange filter (if specified) is applied to the settled date.
    :var BY_VOID_TIME: Order by time of last voided fragment (if any), then by last match time, then placed time, then bet id.
                       Filters out orders which have not been voided. The dateRange filter (if specified) is applied to the voided date.
    """
    BetId = 'BY_BET'
    MarketId = 'BY_MARKET'
    MatchTime = 'BY_MATCH_TIME'
    PlaceTime = 'BY_PLACE_TIME'
    SettleTime = 'BY_SETTLED_TIME'
    VoidTime = 'BY_VOID_TIME'


class SortDir(Enum):
    """
    Sorting by times enum.
    :var EARLIEST_TO_LATEST: Order from earliest value to latest e.g. lowest betId is first in the results.
    :var LATEST_TO_EARLIEST: Order from the latest value to the earliest e.g. highest betId is first in the results.
    """
    TimeAscending = 'EARLIEST_TO_LATEST'
    TimeDescending = 'LATEST_TO_EARLIEST'


class BetStatus(Enum):
    """
    Set bet status to filter for.
    :var SETTLED: A matched bet that was settled normally
    :var VOIDED: A matched bet that was subsequently voided by Betfair, before, during or after settlement
    :var LAPSED: Unmatched bet that was cancelled by Betfair (for example at turn in play).
    :var CANCELLED: Unmatched bet that was cancelled by an explicit customer action.
    """
    Settled = 'SETTLED'
    Voided = 'VOIDED'
    Lapsed = 'LAPSED'
    Cancelled = 'CANCELLED'


class GroupBy(Enum):
    """
    Grouping of P&L reporting
    :var EVENT_TYPE: A roll up of settled P&L, commission paid and number of bet orders, on a specified event type
    :var EVENT: A roll up of settled P&L, commission paid and number of bet orders, on a specified event
    :var MARKET: A roll up of settled P&L, commission paid and number of bet orders, on a specified market
    :var SIDE: An averaged roll up of settled P&L, and number of bets, on the specified side of a specified selection within a specified market, that are either settled or voided
    :var BET: The P&L, commission paid, side and regulatory information etc, about each individual bet order
    """
    EventType = 'EVENT_TYPE'
    Event = 'EVENT'
    Market = 'MARKET'
    Side = 'SIDE'
    Bet = 'BET'


class OrderType(Enum):
    """
    Define order type in sending orders to exchange.
    :var LIMIT: A normal exchange limit order for immediate execution
    :var LIMIT_ON_CLOSE: Limit order for the auction (SP)
    :var MARKET_ON_CLOSE: Market order for the auction (SP)
    """
    LimitOrder = 'LIMIT'
    LimitOnClose = 'LIMIT_ON_CLOSE'
    MarketOnClose = 'MARKET_ON_CLOSE'


class PersistenceType(Enum):
    """
    Description supplied to tell exchange how to handle bet.
    :var LAPSE: Lapse the order when the market is turned in-play
    :var PERSIST: Persist the order to in-play. The bet will be place automatically into the in-play market at the start of the event.
    :var MARKET_ON_CLOSE: Put the order into the auction (SP) at turn-in-play
    """
    Kill = 'LAPSE'
    Keep = 'PERSIST'
    ClosePrice = 'MARKET_ON_CLOSE'


class Wallet(Enum):
    """
    Wallet to check for accounts purposes.
    :var UK: The UK Exchange wallet
    :var AUSTRALIAN: The Australian Exchange wallet - THIS IS NOW DEPRECATED
    """
    UK = 'UK'
    Aus = 'AUSTRALIAN'


class IncludeItem(Enum):
    """
    Items to include for transaction reporting.
    :var ALL: Include all items
    :var DEPOSITS_WITHDRAWALS: Include payments only
    :var EXCHANGE: Include exchange bets only
    :var POKER_ROOM: Include poker transactions only
    """
    All = 'ALL'
    Banking = 'DEPOSITS_WITHDRAWALS'
    Exchange = 'EXCHANGE'
    Poker = 'POKER_ROOM'


class OrderStatus(Enum):
    """
    Status of orders sent, in processing or completed at the exchange.
    :var PENDING: An asynchronous order is yet to be processed. Once the bet has been processed by the exchange (including waiting for any in-play delay),
                  the result will be reported and available on the  Exchange Stream API and API NG. Not a valid search criteria on MarketFilter
    :var EXECUTION_COMPLETE: An order that does not have any remaining unmatched portion.
    :var EXECUTABLE: An order that has a remaining unmatched portion.
    :var EXPIRED: The order is no longer available for execution due to its time in force constraint. Not a valid search criteria on MarketFilter.
                  In the case of FILL_OR_KILL orders, this means the order has been killed because it could not be filled to your specifications.
    """
    Executed = 'EXECUTION_COMPLETE'
    AtExchange = 'EXECUTABLE'
    Expired = 'EXPIRED'
    Pending = 'PENDING'


class TimeInForce(Enum):
    """
    Used to define an order as fill and/or kill.
    :var FILL_OR_KILL: Execute the transaction immediately and completely/between minFillSize and size or killed.
    """
    FillOrKill = 'FILL_OR_KILL'


class BetTargetType(Enum):
    """
    Specify a bet to be for a specific payout or profit.
    :var BACKERS_PROFIT: The payout requested minus the calculated size at which this LimitOrder is to be placed
    :var PAYOUT: The total payout requested on a LimitOrder
    """
    Payout = 'PAYOUT'
    Profit = 'BACKERS_PROFIT'


class MarketBettingType(Enum):
    """
    Specifying the market type on which a bet is to be placed.
    :var ODDS: Odds Market - Any market that doesn't fit any any of the below categories.
    :var LINE: Line Market - Now Deprecated
    :var RANGE: Range Market - Now Deprecated
    :var ASIAN_HANDICAP_DOUBLE_LINE: Asian Handicap Market - A traditional Asian handicap market. Can be identified by marketType ASIAN_HANDICAP
    :var ASIAN_HANDICAP_SINGLE_LINE: Asian Single Line Market - A market in which there can be 0 or multiple winners. e,.g marketType TOTAL_GOALS
    :var FIXED_ODDS: Sportsbook Odds Market. This type is deprecated and will be removed in future releases,
                     when Sportsbook markets will be represented as ODDS market but with a different product type.
    """
    Odds = 'ODDS'
    Line = 'LINE'
    Range = 'RANGE'
    AsianDouble = 'ASIAN_HANDICAP_DOUBLE_LINE'
    AsianSingle = 'ASIAN_HANDICAP_SINGLE_LINE'
    FixedOdds = 'FIXED_ODDS'


class Exchange(Enum):
    """Exchange location to point to."""
    AUS = 'AUS'
    UK = 'UK'