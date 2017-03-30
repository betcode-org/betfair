import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..filters import (
    market_filter,
    time_range,
)
from ..utils import clean_locals


class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.EventTypeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.CompetitionResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, params=None, filter=market_filter(), granularity='DAYS', session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str granularity: granularity filter
        :param requests.session session: Requests session object

        :rtype: list[resources.TimeRangeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.EventResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketTypeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.CountryResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, params=None, filter=market_filter(), locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.VenueResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, params=None, filter=market_filter(), marketProjection=None, sort=None,
                              maxResults=1, locale=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param list marketProjection: the type and amount of data returned about the market
        :param str sort: the order of the results
        :param int maxResults: must be greater than 0 and less than or equal to 1000
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketCatalogue]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)

    def list_market_book(self, params=None, marketIds=None, priceProjection=None, orderProjection=None,
                         matchProjection=None, includeOverallPosition=None, partitionMatchedByStrategyRef=None,
                         customerStrategyRefs=None, currencyCode=None, matchedSince=None, betIds=None, locale=None,
                         session=None):
        """
        :param dict params: json request, will be default if provided
        :param dict filter: market_filter
        :param list marketIds:
        :param dict priceProjection:
        :param str orderProjection:
        :param str matchProjection:
        :param str orderProjection:
        :param bool includeOverallPosition:
        :param bool partitionMatchedByStrategyRef:
        :param list customerStrategyRefs:
        :param str currencyCode:
        :param str matchedSince: #todo str?
        :param list betIds:
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketBook]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketBook')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketBook, date_time_sent)

    def list_current_orders(self, params=None, betIds=None, marketIds=None, orderProjection=None,
                            customerOrderRefs=None, customerStrategyRefs=None, dateRange=time_range(), orderBy=None,
                            sortDir=None, fromRecord=None, recordCount=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param list betIds:
        :param list marketIds:
        :param str orderProjection:
        :param list customerOrderRefs:
        :param list customerStrategyRefs:
        :param dict dateRange:
        :param str orderBy:
        :param str sortDir:
        :param int fromRecord:
        :param int recordCount:
        :param requests.session session: Requests session object

        :rtype: list[resources.CurrentOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrentOrders, date_time_sent)

    def list_cleared_orders(self, params=None, betStatus='SETTLED', eventTypeIds=None, eventIds=None, marketIds=None,
                            runnerIds=None, betIds=None, customerOrderRefs=None, customerStrategyRefs=None, side=None,
                            settledDateRange=time_range(), groupBy=None, includeItemDescription=None, locale=None,
                            fromRecord=None, recordCount=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str betStatus:
        :param list eventTypeIds:
        :param list eventIds:
        :param list marketIds:
        :param list runnerIds:
        :param list betIds:
        :param list customerOrderRefs:
        :param list customerStrategyRefs:
        :param str side:
        :param dict settledDateRange:
        :param str groupBy:
        :param bool includeItemDescription:
        :param str locale:
        :param int fromRecord:
        :param int recordCount:
        :param requests.session session: Requests session object

        :rtype: list[resources.ClearedOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listClearedOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ClearedOrders, date_time_sent)

    def list_market_profit_and_loss(self, params=None, marketIds=None, includeSettledBets=None, includeBspBets=None,
                                    netOfCommission=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param list marketIds: required
        :param bool includeSettledBets:
        :param bool includeBspBets:
        :param bool netOfCommission:
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketProfitLoss]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketProfitLoss, date_time_sent)

    def place_orders(self, params=None, marketId=None, instructions=None, customerRef=None, marketVersion=None,
                     customerStrategyRef=None, async=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str marketId: required
        :param list instructions: required
        :param str customerRef:
        :param str marketVersion:
        :param str customerStrategyRef:
        :param bool async:
        :param requests.session session: Requests session object

        :rtype: list[resources.PlaceOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'placeOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.PlaceOrders, date_time_sent)

    def cancel_orders(self, params=None, marketId=None, instructions=None, customerRef=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str marketId: required
        :param list instructions: required
        :param str customerRef:
        :param requests.session session: Requests session object

        :rtype: list[resources.CancelOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'cancelOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CancelOrders, date_time_sent)

    def update_orders(self, params=None, marketId=None, instructions=None, customerRef=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str marketId: required
        :param list instructions: required
        :param str customerRef:
        :param requests.session session: Requests session object

        :rtype: list[resources.UpdateOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'updateOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.UpdateOrders, date_time_sent)

    def replace_orders(self, params=None, marketId=None, instructions=None, customerRef=None, marketVersion=None,
                       async=None, session=None):
        """
        :param dict params: json request, will be default if provided
        :param str marketId: required
        :param list instructions: required
        :param str customerRef:
        :param str marketVersion:
        :param str async:
        :param requests.session session: Requests session object

        :rtype: list[resources.ReplaceOrders]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'replaceOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ReplaceOrders, date_time_sent)
