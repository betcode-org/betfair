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
