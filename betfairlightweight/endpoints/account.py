import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..enums import *
from ..utils import clean_locals

class Account(BaseEndpoint):

    URI = 'AccountAPING/v1.0/'
    connect_timeout = 6.05

    def get_account_funds(self, session=None, wallet=Wallet.UK):
        """
        Get account funds for specific wallet.

        :param session: requests session to be used. reduces latency.
        :type session: requests instance.
        :param wallet: Determine whether to get info on UK or Aus wallet (deprecated UK only now).
        :type wallet: BetfairAPI.bin.enums.Wallet
        :returns: Available funds, risk exposure, points and discount information.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountFunds')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountFunds, date_time_sent)

    def get_account_details(self, session=None):
        """
        Get details of the current logged in account.

        :param session: requests session to be used. reduces latency.
        :type session: requests instance.
        :returns: Personal information and account information of the logged in user.
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountDetails')
        response = self.request(method, {}, session)
        return self.process_response(response.json(), resources.AccountDetails, date_time_sent)

    def get_account_statement(self, session=None, fromRecord=0, recordCount=None, itemDateRange=None,
                              includeItem=IncludeItem.All, wallet=Wallet.UK, locale=None):
        """
        Get statement of accounts transactions filtered by specified arguments.

        :param session: requests session to be used. reduces latency.
        :type session: requests instance.
        :param fromRecord: Starting point for records returned
        :type fromRecord: int, default 0
        :param recordCount: Maximum number of records to return, max is 100.
        :type recordCount: int
        :param itemDateRange: TimeRange filter for records to include.
        :type itemDateRange: BetfairAPI.bin.utils.create_timerange
        :param includeItem: Filter transaction items to include.
        :type includeItem: BetfairAPI.bin.enums.IncludeItem
        :param wallet: Determine whether to get info on UK or Aus wallet.
        :type wallet: BetfairAPI.bin.enums.Wallet
        :param locale: Language used for response
        :rtype locale: str
        :returns: Transaction statement breakdown.
        :rtype: Dataframe
        :raises: BetfairAPI.bin.exceptions.ApiError
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountStatement')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountStatementResult, date_time_sent)

    def list_currency_rates(self, session=None, fromCurrency='GBP'):
        """
        Get the rates used in currency conversions from a specified currency.

        :param fromCurrency: only supports GBP at the moment.
        :type fromCurrency: str
        :returns: Exchange rates for a list of currencies covered.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrencyRates')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrencyRate, date_time_sent)

    def transfer_funds(self, session=None, account_from=None, account_to=None):
        """
        *** DEPRECATED *** Transfer funds between aus and uk wallets.

        :param account_from: Wallet to transfer from.
        :type account_from: BetfairAPI.bin.enums.Wallet
        :param account_to: Wallet to transfer to.
        :type account_to: BetfairAPI.bin.enums.Wallet
        :return: Transaction overview and updated account information.
        """
        raise DeprecationWarning('As of 20/09/2016 AUS wallet has been removed, function still available for when '
                                 'accounts are added in 2017.')
        # params = clean_locals(locals())
        # date_time_sent = datetime.datetime.utcnow()
        # method = '%s%s' % (self.URI, 'transferFunds')
        # response = self.request(method, params, session)
        # return self.process_response(response.json(), resources.TransferFunds, date_time_sent)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'account/json-rpc/v1')

