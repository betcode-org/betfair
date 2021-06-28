import unittest

from betfairlightweight import resources


class AccountTest(unittest.TestCase):
    def test_account_funds(self):
        resource = resources.AccountFunds(availableToBetBalance=999)
        assert isinstance(resource, resources.AccountFunds)
        assert resource.available_to_bet_balance == 999

    def test_account_details(self):
        resource = resources.AccountDetails(firstName="POO")
        assert isinstance(resource, resources.AccountDetails)
        assert resource.first_name == "POO"

    def test_account_statement_result(self):
        resource = resources.AccountStatementResult(
            accountStatement=[], moreAvailable=True
        )
        assert isinstance(resource, resources.AccountStatementResult)
        assert resource.account_statement == []
        assert resource.more_available is True

    def test_currency_rate(self):
        resource = resources.CurrencyRate(currencyCode="POO", rate=999)
        assert isinstance(resource, resources.CurrencyRate)
        assert resource.currency_code == "POO"
        assert resource.rate == 999

    def test_transfer_funds(self):
        resource = resources.TransferFunds(transactionId=123)
        assert isinstance(resource, resources.TransferFunds)
        assert resource.transaction_id == 123

    def test_legacy_data(self):
        bet_result = {
            "avgPrice": 13.5,
            "betSize": 13.63,
            "betType": "B",
            "betCategoryType": "E",
            "eventId": 184661684,
            "eventTypeId": 7,
            "fullMarketName": "GB / Bath 23rd Jun/ 20:50 1m2f Hcap",
            "grossBetAmount": 0.0,
            "marketName": "1m2f Hcap",
            "marketType": "O",
            "placedDate": "2021-06-23T19:44:29.000Z",
            "selectionId": 25204971,
            "selectionName": "Volcano Bay",
            "startDate": "2021-06-23T19:50:00.000Z",
            "transactionType": "ACCOUNT_DEBIT",
            "transactionId": 0,
            "winLose": "RESULT_LOST",
            "avgPriceRaw": 13.5,
        }

        resource = resources.LegacyData(**bet_result)
        assert isinstance(resource, resources.LegacyData)
        # exchange sub account trans
        exchange_transfer = {
            "avgPrice": 0.0,
            "betSize": 0.0,
            "betType": "B",
            "betCategoryType": "E",
            "eventId": 0,
            "eventTypeId": 0,
            "fullMarketName": "Cross accounts transfer",
            "grossBetAmount": 0.0,
            "marketType": "NOT_APPLICABLE",
            "placedDate": "2021-06-16T07:47:10.000Z",
            "selectionId": 0,
            "startDate": "0001-01-01T00:00:00.000Z",
            "transactionType": "ACCOUNT_DEBIT",
            "transactionId": 0,
            "winLose": "RESULT_NOT_APPLICABLE",
            "avgPriceRaw": 0.0,
        }

        resource = resources.LegacyData(**exchange_transfer)
        assert isinstance(resource, resources.LegacyData)
        assert resource.market_name is None

        account_debit = {
            "avgPrice": 0.0,
            "betSize": 0.0,
            "betType": "B",
            "betCategoryType": "NONE",
            "commissionRate": "2%",
            "eventId": 184661684,
            "eventTypeId": 7,
            "fullMarketName": "GB / Bath 23rd Jun/ 20:50 1m2f Hcap",
            "grossBetAmount": 1968.17,
            "marketName": "1m2f Hcap",
            "marketType": "O",
            "placedDate": "2021-06-23T19:46:12.000Z",
            "selectionId": 0,
            "startDate": "2021-06-23T19:50:00.000Z",
            "transactionType": "ACCOUNT_DEBIT",
            "transactionId": 0,
            "winLose": "RESULT_NOT_APPLICABLE",
            "avgPriceRaw": 0.0,
        }

        resource = resources.LegacyData(**account_debit)
        assert isinstance(resource, resources.LegacyData)
