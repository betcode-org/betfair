import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..filters import (
    market_filter,
    time_range,
)
from ..utils import clean_locals


class Betting(BaseEndpoint):
    """
    Betting operations.
    """

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of Event Types (i.e. Sports) associated with the markets
        selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.EventTypeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of Competitions (i.e., World Cup 2013) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.CompetitionResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, filter=market_filter(), granularity='DAYS', session=None):
        """
        Returns a list of time ranges in the granularity specified in the
        request (i.e. 3PM to 4PM, Aug 14th to Aug 15th) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str granularity: The granularity of time periods that correspond
        to markets selected by the market filter
        :param requests.session session: Requests session object

        :rtype: list[resources.TimeRangeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of Events (i.e, Reading vs. Man United) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.EventResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketTypeResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of Countries associated with the markets selected by
        the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.CountryResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, filter=market_filter(), locale=None, session=None):
        """
        Returns a list of Venues (i.e. Cheltenham, Ascot) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.VenueResult]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, filter=market_filter(), marketProjection=None, sort=None, maxResults=1,
                              locale=None, session=None):
        """
        Returns a list of information about published (ACTIVE/SUSPENDED) markets
        that does not change (or changes very rarely).

        :param dict filter: The filter to select desired markets
        :param list marketProjection: The type and amount of data returned about the market
        :param str sort: The order of the results
        :param int maxResults: Limit on the total number of results returned, must be greater
        than 0 and less than or equal to 10000
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketCatalogue]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)

    def list_market_book(self, marketIds, priceProjection=None, orderProjection=None,
                         matchProjection=None, includeOverallPosition=None, partitionMatchedByStrategyRef=None,
                         customerStrategyRefs=None, currencyCode=None, matchedSince=None, betIds=None, locale=None,
                         session=None):
        """
        Returns a list of dynamic data about markets. Dynamic data includes prices,
        the status of the market, the status of selections, the traded volume, and
        the status of any orders you have placed in the market

        :param list marketIds: One or more market ids
        :param dict priceProjection: The projection of price data you want to receive in the response
        :param str orderProjection: The orders you want to receive in the response
        :param str matchProjection: If you ask for orders, specifies the representation of matches
        :param bool includeOverallPosition: If you ask for orders, returns matches for each selection
        :param bool partitionMatchedByStrategyRef: If you ask for orders, returns the breakdown of matches
        by strategy for each selection
        :param list customerStrategyRefs: f you ask for orders, restricts the results to orders matching
        any of the specified set of customer defined strategies
        :param str currencyCode: A Betfair standard currency code
        :param str matchedSince: If you ask for orders, restricts the results to orders that have at
        least one fragment matched since the specified date
        :param list betIds: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param str locale: The language used for the response
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketBook]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketBook')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketBook, date_time_sent)

    def list_current_orders(self, betIds=None, marketIds=None, orderProjection=None,
                            customerOrderRefs=None, customerStrategyRefs=None, dateRange=time_range(), orderBy=None,
                            sortDir=None, fromRecord=None, recordCount=None, session=None):
        """
        Returns a list of your current orders.

        :param list betIds: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list marketIds: One or more market ids
        :param str orderProjection: Optionally restricts the results to the specified order status
        :param list customerOrderRefs: Optionally restricts the results to the specified customer order references
        :param list customerStrategyRefs: Optionally restricts the results to the specified customer strategy references
        :param dict dateRange: Optionally restricts the results to be from/to the specified date, these dates
        are contextual to the orders being returned and therefore the dates used to filter on will change
        to placed, matched, voided or settled dates depending on the orderBy
        :param str orderBy: Specifies how the results will be ordered. If no value is passed in, it defaults to BY_BET
        :param str sortDir: Specifies the direction the results will be sorted in
        :param int fromRecord: Specifies the first record that will be returned
        :param int recordCount: Specifies how many records will be returned from the index position 'fromRecord'
        :param requests.session session: Requests session object

        :rtype: resources.CurrentOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrentOrders, date_time_sent)

    def list_cleared_orders(self, betStatus='SETTLED', eventTypeIds=None, eventIds=None, marketIds=None,
                            runnerIds=None, betIds=None, customerOrderRefs=None, customerStrategyRefs=None, side=None,
                            settledDateRange=time_range(), groupBy=None, includeItemDescription=None, locale=None,
                            fromRecord=None, recordCount=None, session=None):
        """
        Returns a list of settled bets based on the bet status,
        ordered by settled date.

        :param str betStatus: Restricts the results to the specified status
        :param list eventTypeIds: Optionally restricts the results to the specified Event Type IDs
        :param list eventIds: Optionally restricts the results to the specified Event IDs
        :param list marketIds: Optionally restricts the results to the specified market IDs
        :param list runnerIds: Optionally restricts the results to the specified Runners
        :param list betIds: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list customerOrderRefs: Optionally restricts the results to the specified customer order references
        :param list customerStrategyRefs: Optionally restricts the results to the specified customer strategy references
        :param str side: Optionally restricts the results to the specified side
        :param dict settledDateRange: Optionally restricts the results to be from/to the specified settled date
        :param str groupBy: How to aggregate the lines, if not supplied then the lowest level is returned
        :param bool includeItemDescription: If true then an ItemDescription object is included in the response
        :param str locale: The language used for the response
        :param int fromRecord: Specifies the first record that will be returned
        :param int recordCount: Specifies how many records will be returned from the index position 'fromRecord'
        :param requests.session session: Requests session object

        :rtype: resources.ClearedOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listClearedOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ClearedOrders, date_time_sent)

    def list_market_profit_and_loss(self, marketIds, includeSettledBets=None, includeBspBets=None,
                                    netOfCommission=None, session=None):
        """
        Retrieve profit and loss for a given list of OPEN markets.

        :param list marketIds: List of markets to calculate profit and loss
        :param bool includeSettledBets: Option to include settled bets (partially settled markets only)
        :param bool includeBspBets: Option to include BSP bets
        :param bool netOfCommission: Option to return profit and loss net of users current commission
        rate for this market including any special tariffs
        :param requests.session session: Requests session object

        :rtype: list[resources.MarketProfitLoss]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketProfitLoss, date_time_sent)

    def place_orders(self, marketId, instructions, customerRef=None, marketVersion=None,
                     customerStrategyRef=None, async=None, session=None):
        """
        Place new orders into market.

        :param str marketId: The market id these orders are to be placed on
        :param list instructions: The number of place instructions
        :param str customerRef: Optional parameter allowing the client to pass a unique string
        (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param str marketVersion: Optional parameter allowing the client to specify which
        version of the market the orders should be placed on
        :param str customerStrategyRef: An optional reference customers can use to specify
        which strategy has sent the order
        :param bool async: An optional flag (not setting equates to false) which specifies if
        the orders should be placed asynchronously
        :param requests.session session: Requests session object

        :rtype: resources.PlaceOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'placeOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.PlaceOrders, date_time_sent)

    def cancel_orders(self, marketId, instructions, customerRef=None, session=None):
        """
        Cancel all bets OR cancel all bets on a market OR fully or partially
        cancel particular orders on a market.

        :param str marketId: If marketId and betId aren't supplied all bets are cancelled
        :param list instructions: All instructions need to be on the same market
        :param str customerRef: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object

        :rtype: resources.CancelOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'cancelOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CancelOrders, date_time_sent)

    def update_orders(self, marketId, instructions, customerRef=None, session=None):
        """
        Update non-exposure changing field.

        :param str marketId: The market id these orders are to be placed on
        :param list instructions: The update instructions
        :param str customerRef: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object

        :rtype: resources.UpdateOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'updateOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.UpdateOrders, date_time_sent)

    def replace_orders(self, marketId, instructions, customerRef=None, marketVersion=None,
                       async=None, session=None):
        """
        This operation is logically a bulk cancel followed by a bulk place.
        The cancel is completed first then the new orders are placed.

        :param str marketId: The market id these orders are to be placed on
        :param list instructions: The number of replace instructions.  The limit
        of replace instructions per request is 60
        :param str customerRef: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param str marketVersion: Optional parameter allowing the client to specify
        which version of the market the orders should be placed on
        :param str async: An optional flag (not setting equates to false) which specifies
        if the orders should be replaced asynchronously
        :param requests.session session: Requests session object

        :rtype: resources.ReplaceOrders
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'replaceOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ReplaceOrders, date_time_sent)
