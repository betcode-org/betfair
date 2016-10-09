import datetime

from .baseendpoint import BaseEndpoint
from .. import resources


class Account(BaseEndpoint):

    URI = 'AccountAPING/v1.0/'
    connect_timeout = 6.05

    def get_account_funds(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountFunds')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountFunds, date_time_sent)

    def get_account_details(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountDetails')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountDetails, date_time_sent)

    def get_account_statement(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'getAccountStatement')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AccountStatementResult, date_time_sent)

    def list_currency_rates(self, params=None, session=None):
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
