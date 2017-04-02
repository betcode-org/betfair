import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals
from ..filters import time_range


class Account(BaseEndpoint):
    """
    Account operations.
    """

    URI = 'AccountAPING/v1.0/'
    connect_timeout = 6.05

    def get_account_funds(self, wallet=None, session=None):
        """
        Get available to bet amount.

        :param str wallet: Name of the wallet in question
        :param requests.session session: Requests session object

        :rtype: resources.AccountFunds
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountFunds')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountFunds, date_time_sent)

    def get_account_details(self, session=None):
        """
        Returns the details relating your account, including your discount
        rate and Betfair point balance.

        :param requests.session session: Requests session object

        :rtype: resources.AccountDetails
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountDetails')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountDetails, date_time_sent)

    def get_account_statement(self, locale=None, fromRecord=None, recordCount=None, itemDateRange=time_range(),
                              includeItem=None, wallet=None, session=None):
        """
        Get account statement.

        :param str locale: The language to be used where applicable.
        :param int fromRecord: Specifies the first record that will be returned
        :param int recordCount: Specifies the maximum number of records to be returned.
        :param dict itemDateRange: Return items with an itemDate within this date range.
        :param str includeItem: Which items to include, if not specified then defaults to ALL.
        :param str wallet: Which wallet to return statementItems for.
        :param requests.session session: Requests session object

        :rtype: resources.AccountStatementResult
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountStatement')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountStatementResult, date_time_sent)

    def list_currency_rates(self, fromCurrency=None, session=None):
        """
        Returns a list of currency rates based on given currency

        :param str fromCurrency: The currency from which the rates are computed
        :param requests.session session: Requests session object

        :rtype: list[resources.CurrencyRate]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrencyRates')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrencyRate, date_time_sent)

    def transfer_funds(self, session=None):
        """
        Transfer funds between the UK Exchange and other wallets

        :param requests.session session: Requests session object

        :rtype: resources.TransferFunds
        """
        raise DeprecationWarning(
            'As of 20/09/2016 AUS wallet has been removed, function still available for when '
            'accounts are added in 2017.')

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'account/json-rpc/v1')
