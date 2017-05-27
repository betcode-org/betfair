from __future__ import print_function

import unittest
import datetime

from betfairlightweight import resources
from betfairlightweight.resources.accountresources import LegacyData

from tests.tools import create_mock_json


class AccountTest(unittest.TestCase):

    def test_account_funds(self):
        resource = resources.AccountFunds(availableToBetBalance=999)
        assert isinstance(resource, resources.AccountFunds)
        assert resource.available_to_bet_balance == 999

    def test_account_details(self):
        resource = resources.AccountDetails(firstName='POO')
        assert isinstance(resource, resources.AccountDetails)
        assert resource.first_name == 'POO'

    def test_account_statement_result(self):
        resource = resources.AccountStatementResult(accountStatement=[], moreAvailable=True)
        assert isinstance(resource, resources.AccountStatementResult)
        assert resource.account_statement == []
        assert resource.more_available is True

    def test_currency_rate(self):
        resource = resources.CurrencyRate(currencyCode='POO', rate=999)
        assert isinstance(resource, resources.CurrencyRate)
        assert resource.currency_code == 'POO'
        assert resource.rate == 999

    def test_transfer_funds(self):
        resource = resources.TransferFunds(transactionId=123)
        assert isinstance(resource, resources.TransferFunds)
        assert resource.transaction_id == 123

    def test_legacy_data(self):
        legacy_data = LegacyData('avgPrice','betCategoryType', 'betSize', 'betType', 'eventId', 
            'eventTypeId', 'fullMarketName', 'marketName', 'grossBetAmount', 'transactionId', 'marketType',
            '2017-07-25 12:34', 'selectionId', '2017-08-09 10:20', 'transactionType','winLose', 'selectionName', 'commissionRate')
        assert legacy_data.avg_price == 'avgPrice'
        assert legacy_data.bet_category_type == 'betCategoryType'
        assert legacy_data.bet_size == 'betSize'
        assert legacy_data.bet_type == 'betType'
        assert legacy_data.event_id == 'eventId'
        assert legacy_data.event_type_id == 'eventTypeId'
        assert legacy_data.full_market_name == 'fullMarketName'
        assert legacy_data.market_name == 'marketName'
        assert legacy_data.gross_bet_amount == 'grossBetAmount'
        assert legacy_data.transaction_id == 'transactionId'
        assert legacy_data.market_type == 'marketType'
        assert legacy_data.placed_date == datetime.datetime(2017,7,25,12,34)
        assert legacy_data.selection_id == 'selectionId'
        assert legacy_data.start_date == datetime.datetime(2017,8,9,10,20)
        assert legacy_data.transaction_type == 'transactionType'
        assert legacy_data.win_lose == 'winLose'
        assert legacy_data.selection_name == 'selectionName'
        assert legacy_data.commission_rate == 'commissionRate'
