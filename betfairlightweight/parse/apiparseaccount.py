from ..parse.models import BetfairModel
from ..utils import strp_betfair_time


class AccountFunds(BetfairModel):

    def __init__(self, date_time_sent, raw_response, account_funds):
        super(AccountFunds, self).__init__(date_time_sent, raw_response)
        self.available_to_bet_balance = account_funds.get('availableToBetBalance')
        self.discount_rate = account_funds.get('discountRate')
        self.exposure = account_funds.get('exposure')
        self.exposure_limit = account_funds.get('exposureLimit')
        self.points_balance = account_funds.get('pointsBalance')
        self.retained_commission = account_funds.get('retainedCommission')
        self.wallet = account_funds.get('wallet')


class AccountDetails(BetfairModel):

    def __init__(self, date_time_sent, raw_response, account_details):
        super(AccountDetails, self).__init__(date_time_sent, raw_response)
        self.country_code = account_details.get('countryCode')
        self.currency_code = account_details.get('currencyCode')
        self.discount_rate = account_details.get('discountRate')
        self.first_name = account_details.get('firstName')
        self.last_name = account_details.get('lastName')
        self.locale_code = account_details.get('localeCode')
        self.points_balance = account_details.get('pointsBalance')
        self.region = account_details.get('region')
        self.timezone = account_details.get('timezone')


class AccountStatement(BetfairModel):

    def __init__(self, date_time_sent, raw_response, account_statement):
        super(AccountStatement, self).__init__(date_time_sent, raw_response)
        self.more_available = account_statement.get('moreAvailable')
        self.account_statement = [AccountStatementStatement(statement)
                                  for statement in account_statement.get('accountStatement')]


class AccountStatementStatement:

    def __init__(self, statement):
        self.amount = statement.get('amount')
        self.balance = statement.get('balance')
        self.item_class = statement.get('itemClass')
        self.item_class_data = statement.get('itemClassData')
        self.item_date = strp_betfair_time(statement.get('itemDate'))
        self.legacy_data = AccountStatementLegacyData(statement.get('legacyData'))
        self.ref_id = statement.get('refId')


class AccountStatementLegacyData:

    def __init__(self, legacy_data):
        self.avg_price = legacy_data.get('avgPrice')
        self.bet_category_type = legacy_data.get('betCategoryType')
        self.bet_size = legacy_data.get('betSize')
        self.bet_type = legacy_data.get('betType')
        self.event_id = legacy_data.get('eventId')
        self.event_type_id = legacy_data.get('eventTypeId')
        self.full_market_name = legacy_data.get('fullMarketName')
        self.gross_bet_amount = legacy_data.get('grossBetAmount')


class CurrencyRate(BetfairModel):

    def __init__(self, date_time_sent, raw_response, currency_rate):
        super(CurrencyRate, self).__init__(date_time_sent, raw_response)
        self.currency_code = currency_rate.get('currencyCode')
        self.rate = currency_rate.get('rate')


class TransferFunds(BetfairModel):

    def __init__(self, date_time_sent, raw_response, transfer_funds):
        super(TransferFunds, self).__init__(date_time_sent, raw_response)
        self.transaction_id = transfer_funds.get('transactionId')
