import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals
from ..filters import time_range


class Account(BaseEndpoint):

    URI = 'AccountAPING/v1.0/'
    connect_timeout = 6.05

    def get_account_funds(self, params=None, wallet=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str wallet:
        :param requests.session session: Requests session object

        :rtype: resources.AccountFunds
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountFunds')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountFunds, date_time_sent)

    def get_account_details(self, params=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param requests.session session: Requests session object

        :rtype: resources.AccountDetails
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountDetails')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountDetails, date_time_sent)

    def get_account_statement(self, params=None, locale=None, fromRecord=None, recordCount=None,
                              itemDateRange=time_range(), includeItem=None, wallet=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str locale:
        :param int fromRecord:
        :param int recordCount:
        :param dict itemDateRange:
        :param str includeItem:
        :param str wallet:

        :rtype: resources.AccountStatement
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountStatement')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountStatementResult, date_time_sent)

    def list_currency_rates(self, params=None, fromCurrency=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str fromCurrency:

        :rtype: list[resources.CurrencyRate]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrencyRates')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrencyRate, date_time_sent)

    def transfer_funds(self, params=None, session=None):
        raise DeprecationWarning('As of 20/09/2016 AUS wallet has been removed, function still available for when '
                                 'accounts are added in 2017.')
        # date_time_sent = datetime.datetime.utcnow()
        # method = '%s%s' % (self.URI, 'transferFunds')
        # response = self.request(method, params, session)
        # return self.process_response(response.json(), resources.TransferFunds, date_time_sent)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'account/json-rpc/v1')
