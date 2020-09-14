import requests
from typing import Union, List

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals
from ..filters import time_range


class Account(BaseEndpoint):
    """
    Account operations.
    """

    URI = "AccountAPING/v1.0/"
    connect_timeout = 6.05

    def get_account_funds(
        self,
        wallet: str = None,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[dict, resources.AccountFunds]:
        """
        Get available to bet amount.

        :param str wallet: Name of the wallet in question
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.AccountFunds
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "getAccountFunds")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.AccountFunds, elapsed_time, lightweight
        )

    def get_account_details(
        self, session: requests.Session = None, lightweight: bool = None
    ) -> Union[dict, resources.AccountDetails]:
        """
        Returns the details relating your account, including your discount
        rate and Betfair point balance.

        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.AccountDetails
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "getAccountDetails")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.AccountDetails, elapsed_time, lightweight
        )

    def get_account_statement(
        self,
        locale: str = None,
        from_record: int = None,
        record_count: int = None,
        item_date_range: dict = time_range(),
        include_item: str = None,
        wallet: str = None,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[dict, resources.AccountStatementResult]:
        """
        Get account statement.

        :param str locale: The language to be used where applicable.
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies the maximum number of records to be returned.
        :param dict item_date_range: Return items with an itemDate within this date range.
        :param str include_item: Which items to include, if not specified then defaults to ALL.
        :param str wallet: Which wallet to return statementItems for.
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.AccountStatementResult
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "getAccountStatement")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.AccountStatementResult,
            elapsed_time,
            lightweight,
        )

    def list_currency_rates(
        self,
        from_currency: str = None,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[dict, List[resources.CurrencyRate]]:
        """
        Returns a list of currency rates based on given currency

        :param str from_currency: The currency from which the rates are computed
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.CurrencyRate]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listCurrencyRates")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.CurrencyRate, elapsed_time, lightweight
        )

    def transfer_funds(self, session: requests.Session = None) -> None:
        """
        Transfer funds between the UK Exchange and other wallets

        :param requests.session session: Requests session object

        :rtype: resources.TransferFunds
        """
        raise DeprecationWarning(
            "As of 20/09/2016 AUS wallet has been removed, function still available for when "
            "accounts are added in 2017."
        )

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.api_uri, "account/json-rpc/v1")
