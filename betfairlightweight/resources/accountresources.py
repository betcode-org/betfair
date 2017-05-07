from .baseresource import BaseResource


class AccountFunds(BaseResource):

    def __init__(self, **kwargs):
        super(AccountFunds, self).__init__(**kwargs)
        self.available_to_bet_balance = kwargs.get('availableToBetBalance')
        self.discount_rate = kwargs.get('discountRate')
        self.exposure = kwargs.get('exposure')
        self.exposure_limit = kwargs.get('exposureLimit')
        self.points_balance = kwargs.get('pointsBalance')
        self.retained_commission = kwargs.get('retainedCommission')
        self.wallet = kwargs.get('wallet')


class AccountDetails(BaseResource):

    def __init__(self, **kwargs):
        super(AccountDetails, self).__init__(**kwargs)
        self.country_code = kwargs.get('countryCode')
        self.currency_code = kwargs.get('currencyCode')
        self.discount_rate = kwargs.get('discountRate')
        self.first_name = kwargs.get('firstName')
        self.last_name = kwargs.get('lastName')
        self.locale_code = kwargs.get('localeCode')
        self.points_balance = kwargs.get('pointsBalance')
        self.region = kwargs.get('region')
        self.timezone = kwargs.get('timezone')


class LegacyData(object):

    def __init__(self, avgPrice, betCategoryType, betSize, betType, eventId, eventTypeId, fullMarketName, marketName,
                 grossBetAmount, transactionId, marketType, placedDate, selectionId, startDate, transactionType,
                 winLose, selectionName=None, commissionRate=None):
        self.avg_price = avgPrice
        self.bet_category_type = betCategoryType
        self.bet_size = betSize
        self.bet_type = betType
        self.event_id = eventId
        self.event_type_id = eventTypeId
        self.full_market_name = fullMarketName
        self.gross_bet_amount = grossBetAmount
        self.market_name = marketName
        self.transaction_id = transactionId
        self.market_type = marketType
        self.placed_date = BaseResource.strip_datetime(placedDate)
        self.selection_id = selectionId
        self.start_date = BaseResource.strip_datetime(startDate)
        self.transaction_type = transactionType
        self.win_lose = winLose
        self.selection_name = selectionName
        self.commission_rate = commissionRate


class AccountStatement(object):

    def __init__(self, amount, balance, itemClass, itemClassData, itemDate, refId, legacyData):
        self.amount = amount
        self.balance = balance
        self.item_class = itemClass
        self.item_class_data = itemClassData
        self.item_date = BaseResource.strip_datetime(itemDate)
        self.ref_id = refId
        self.legacy_data = LegacyData(**legacyData)


class AccountStatementResult(BaseResource):

    def __init__(self, **kwargs):
        super(AccountStatementResult, self).__init__(**kwargs)
        self.more_available = kwargs.get('moreAvailable')
        self.account_statement = [AccountStatement(**i) for i in kwargs.get('accountStatement')]


class CurrencyRate(BaseResource):

    def __init__(self, **kwargs):
        super(CurrencyRate, self).__init__(**kwargs)
        self.currency_code = kwargs.get('currencyCode')
        self.rate = kwargs.get('rate')


class TransferFunds(BaseResource):

    def __init__(self, **kwargs):
        super(TransferFunds, self).__init__(**kwargs)
        self.transaction_id = kwargs.get('transactionId')
