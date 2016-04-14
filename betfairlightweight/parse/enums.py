from enum import Enum


class MockParams(Enum):
    list_event_types = {'filter': {}}
    list_competitions = {'filter': {}}
    list_time_ranges = {'filter': {},
                        'granularity': 'DAYS'}
    list_events = {'filter': {}}
    list_market_types = {'filter': {}}
    list_countries = {'filter': {}}
    list_venues = {'filter': {}}
    list_market_catalogue = {'filter': {},
                             'maxResults': '1'}
    list_market_book = {'marketIds': ['1.122618187']}
    place_orders = {}
    cancel_orders = {}
    update_orders = {}
    replace_orders = {}
    list_current_orders = {'dateRange': {}}
    list_cleared_orders = {'betStatus': 'SETTLED',
                           'settledDateRange': {},
                           'recordCount': '1000'}
    list_market_profit_and_loss = {'marketIds': ['1.122617964']}
    list_race_status = {}
    get_account_funds = {'wallet': None}
    get_account_details = {}
    get_account_statement = {'itemDateRange': {},
                             'includeItem': 'ALL'}
    list_currency_rates = {'fromCurrency': 'GBP'}
    transfer_funds = {'from': 'UK',
                      'to': 'AUSTRALIAN',
                      'amount': '0.00'}


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


# class GenericJsonRpcExceptions(Enum):
#     -32700 = 'Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.'
#     -32601 = 'Method not found'
#     -32602 = 'Problem parsing the parameters, or a mandatory parameter was not found'
#     -32603 = 'Internal JSON-RPC error'


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
    INVALID_CONNECTIVITY_TO_REGULATOR_DK = "The DK regulator cannot be accessed due to some internal problems in the system behind or in at regulator; timeout cases included."
    NOT_AUTHORIZED_BY_REGULATOR_DK = "The user identified by the given credentials is not authorized in the DKs jurisdictions due to the regulators policies. Ex = the user for which this session should be created is not allowed to act(play bet) in the DKs jurisdiction."
    INVALID_CONNECTIVITY_TO_REGULATOR_IT = "The IT regulator cannot be accessed due to some internal problems in the system behind or in at regulator; timeout cases included."
    NOT_AUTHORIZED_BY_REGULATOR_IT = "The user identified by the given credentials is not authorized in the ITs jurisdictions due to the regulators policies. Ex = the user for which this session should be created is not allowed to act(play bet) in the ITs jurisdiction."
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
    INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRE = "The latest international terms and conditions must be accepted prior to logging in."
    EMAIL_LOGIN_NOT_ALLOWED = "This account has not opted in to log in with the email"
    MULTIPLE_USERS_WITH_SAME_CREDENTIAL = "There is more than one account with the same credential"
    ACCOUNT_PENDING_PASSWORD_CHANGE = "The account must undergo password recovery to reactivate"
    TEMPORARY_BAN_TOO_MANY_REQUEST = "The limit for successful login requests per minute has been exceeded. New login attempts will be banned for 20 minutes"
