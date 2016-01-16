import logging
from utils import key_check, strp_betfair_time, key_check_datetime


class AccountFunds:

    def __init__(self, account_funds):
        self.available_to_bet_balance = account_funds['availableToBetBalance']
        self.discount_rate = account_funds['discountRate']
        self.exposure = account_funds['exposure']
        self.exposure_limit = account_funds['exposureLimit']
        self.points_balance = account_funds['pointsBalance']
        self.retained_commission = account_funds['retainedCommission']
        self.wallet = account_funds['wallet']


class AccountDetails:

    def __init__(self, account_details):
        self.country_code = account_details['countryCode']
        self.currency_code = account_details['currencyCode']
        self.discount_rate = account_details['discountRate']
        self.first_name = account_details['firstName']
        self.last_name = account_details['lastName']
        self.locale_code = account_details['localeCode']
        self.points_balance = account_details['pointsBalance']
        self.region = account_details['region']
        self.timezone = account_details['timezone']


class AccountStatement:

    def __init__(self, account_statement):
        self.more_available = account_statement['moreAvailable']
        self.account_statement = [AccountStatementStatement(statement)
                                  for statement in account_statement['accountStatement']]

class AccountStatementStatement:

    def __init__(self, statement):
        self.amount = statement['amount']
        self.balance = statement['balance']
        self.item_class = statement['itemClass']
        self.item_class_data = statement['itemClassData']
        self.item_date = strp_betfair_time(statement['itemDate'])
        self.legacy_data = AccountStatementLegacyData(statement['legacyData'])
        self.ref_id = statement['refId']


class AccountStatementLegacyData:

    def __init__(self, legacy_data):
        self.avg_price = legacy_data['avgPrice']
        self.bet_category_type = legacy_data['betCategoryType']
        self.bet_size = legacy_data['betSize']
        self.bet_type = legacy_data['betType']
        self.event_id = legacy_data['eventId']
        self.event_type_id = legacy_data['eventTypeId']
        self.full_market_name = legacy_data['fullMarketName']
        self.gross_bet_amount = legacy_data['grossBetAmount']


class CurrencyRate:

    def __init__(self, currency_rate):
        self.currency_code = currency_rate['currencyCode']
        self.rate = currency_rate['rate']


class TransferFunds:

    def __init__(self, transfer_funds):
        self.transaction_id = transfer_funds['transactionId']
