from .baseresource import BaseResource


class AccountFunds(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'account_funds'
        attributes = {
            'availableToBetBalance': 'available_to_bet_balance',
            'discountRate': 'discount_rate',
            'exposure': 'exposure',
            'exposureLimit': 'exposure_limit',
            'pointsBalance': 'points_balance',
            'retainedCommission': 'retained_commission',
            'wallet': 'wallet'
        }


class AccountDetails(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'account_details'
        attributes = {
            'countryCode': 'country_code',
            'currencyCode': 'currency_code',
            'discountRate': 'discount_rate',
            'firstName': 'first_name',
            'lastName': 'last_name',
            'localeCode': 'locale_code',
            'pointsBalance': 'points_balance',
            'region': 'region',
            'timezone': 'timezone'
        }


class LegacyData(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'legacy_data'
        attributes = {
            'avgPrice': 'avg_price',
            'betCategoryType': 'bet_category_type',
            'betSize': 'bet_size',
            'betType': 'bet_type',
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'fullMarketName': 'full_market_name',
            'grossBetAmount': 'gross_bet_amount'
        }


class AccountStatement(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'account_statement'
        attributes = {
            'amount': 'amount',
            'balance': 'balance',
            'itemClass': 'item_class',
            'itemClassData': 'item_class_data',
            'itemDate': 'item_date',
            'refId': 'ref_id'
        }
        sub_resources = {
            'legacyData': LegacyData
        }
        datetime_attributes = (
            'itemDate',
        )


class AccountStatementResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'account_statement_result'
        attributes = {
            'moreAvailable': 'more_available'
        }
        sub_resources = {
            'accountStatement': AccountStatement
        }


class CurrencyRate(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'currency_rate'
        attributes = {
            'currencyCode': 'currency_code',
            'rate': 'rate'
        }


class TransferFunds(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'transfer_funds'
        attributes = {
            'transactionId': 'transaction_id'
        }
