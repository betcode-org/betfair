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

    def list_event_types(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of Event Types (i.e. Sports) associated with the markets
        selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.EventTypeResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listEventTypes')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.EventTypeResult, elapsed_time, lightweight)

    def list_competitions(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of Competitions (i.e., World Cup 2013) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.CompetitionResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listCompetitions')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.CompetitionResult, elapsed_time, lightweight)

    def list_time_ranges(self, filter=market_filter(), granularity='DAYS', session=None, lightweight=None):
        """
        Returns a list of time ranges in the granularity specified in the
        request (i.e. 3PM to 4PM, Aug 14th to Aug 15th) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str granularity: The granularity of time periods that correspond
        to markets selected by the market filter
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.TimeRangeResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listTimeRanges')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.TimeRangeResult, elapsed_time, lightweight)

    def list_events(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of Events (i.e, Reading vs. Man United) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.EventResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listEvents')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.EventResult, elapsed_time, lightweight)

    def list_market_types(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketTypeResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listMarketTypes')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.MarketTypeResult, elapsed_time, lightweight)

    def list_countries(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of Countries associated with the markets selected by
        the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.CountryResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listCountries')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.CountryResult, elapsed_time, lightweight)

    def list_venues(self, filter=market_filter(), locale=None, session=None, lightweight=None):
        """
        Returns a list of Venues (i.e. Cheltenham, Ascot) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.VenueResult]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listVenues')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.VenueResult, elapsed_time, lightweight)

    def list_market_catalogue(self, filter=market_filter(), market_projection=None, sort=None, max_results=1,
                              locale=None, session=None, lightweight=None):
        """
        Returns a list of information about published (ACTIVE/SUSPENDED) markets
        that does not change (or changes very rarely).

        :param dict filter: The filter to select desired markets
        :param list market_projection: The type and amount of data returned about the market
        :param str sort: The order of the results
        :param int max_results: Limit on the total number of results returned, must be greater
        than 0 and less than or equal to 10000
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketCatalogue]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.MarketCatalogue, elapsed_time, lightweight)

    def list_market_book(self, market_ids, price_projection=None, order_projection=None,
                         match_projection=None, include_overall_position=None, partition_matched_by_strategy_ref=None,
                         customer_strategy_refs=None, currency_code=None, matched_since=None, bet_ids=None, locale=None,
                         session=None, lightweight=None):
        """
        Returns a list of dynamic data about markets. Dynamic data includes prices,
        the status of the market, the status of selections, the traded volume, and
        the status of any orders you have placed in the market

        :param list market_ids: One or more market ids
        :param dict price_projection: The projection of price data you want to receive in the response
        :param str order_projection: The orders you want to receive in the response
        :param str match_projection: If you ask for orders, specifies the representation of matches
        :param bool include_overall_position: If you ask for orders, returns matches for each selection
        :param bool partition_matched_by_strategy_ref: If you ask for orders, returns the breakdown of matches
        by strategy for each selection
        :param list customer_strategy_refs: If you ask for orders, restricts the results to orders matching
        any of the specified set of customer defined strategies
        :param str currency_code: A Betfair standard currency code
        :param str matched_since: If you ask for orders, restricts the results to orders that have at
        least one fragment matched since the specified date
        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketBook]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listMarketBook')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.MarketBook, elapsed_time, lightweight)

    def list_current_orders(self, bet_ids=None, market_ids=None, order_projection=None, customer_order_refs=None,
                            customer_strategy_refs=None, date_range=time_range(), order_by=None, sort_dir=None,
                            from_record=None, record_count=None, session=None, lightweight=None):
        """
        Returns a list of your current orders.

        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list market_ids: One or more market ids
        :param str order_projection: Optionally restricts the results to the specified order status
        :param list customer_order_refs: Optionally restricts the results to the specified customer order references
        :param list customer_strategy_refs: Optionally restricts the results to the specified customer strategy
        references
        :param dict date_range: Optionally restricts the results to be from/to the specified date, these dates
        are contextual to the orders being returned and therefore the dates used to filter on will change
        to placed, matched, voided or settled dates depending on the orderBy
        :param str order_by: Specifies how the results will be ordered. If no value is passed in, it defaults to BY_BET
        :param str sort_dir: Specifies the direction the results will be sorted in
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies how many records will be returned from the index position 'fromRecord'
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.CurrentOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.CurrentOrders, elapsed_time, lightweight)

    def list_cleared_orders(self, bet_status='SETTLED', event_type_ids=None, event_ids=None, market_ids=None,
                            runner_ids=None, bet_ids=None, customer_order_refs=None, customer_strategy_refs=None,
                            side=None, settled_date_range=time_range(), group_by=None, include_item_description=None,
                            locale=None, from_record=None, record_count=None, session=None, lightweight=None):
        """
        Returns a list of settled bets based on the bet status,
        ordered by settled date.

        :param str bet_status: Restricts the results to the specified status
        :param list event_type_ids: Optionally restricts the results to the specified Event Type IDs
        :param list event_ids: Optionally restricts the results to the specified Event IDs
        :param list market_ids: Optionally restricts the results to the specified market IDs
        :param list runner_ids: Optionally restricts the results to the specified Runners
        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list customer_order_refs: Optionally restricts the results to the specified customer order references
        :param list customer_strategy_refs: Optionally restricts the results to the specified customer strategy
        references
        :param str side: Optionally restricts the results to the specified side
        :param dict settled_date_range: Optionally restricts the results to be from/to the specified settled date
        :param str group_by: How to aggregate the lines, if not supplied then the lowest level is returned
        :param bool include_item_description: If true then an ItemDescription object is included in the response
        :param str locale: The language used for the response
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies how many records will be returned from the index position 'fromRecord'
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.ClearedOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listClearedOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.ClearedOrders, elapsed_time, lightweight)

    def list_market_profit_and_loss(self, market_ids, include_settled_bets=None, include_bsp_bets=None,
                                    net_of_commission=None, session=None, lightweight=None):
        """
        Retrieve profit and loss for a given list of OPEN markets.

        :param list market_ids: List of markets to calculate profit and loss
        :param bool include_settled_bets: Option to include settled bets (partially settled markets only)
        :param bool include_bsp_bets: Option to include BSP bets
        :param bool net_of_commission: Option to return profit and loss net of users current commission
        rate for this market including any special tariffs
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketProfitLoss]
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.MarketProfitLoss, elapsed_time, lightweight)

    def place_orders(self, market_id, instructions, customer_ref=None, market_version=None,
                     customer_strategy_ref=None, async=None, session=None, lightweight=None):
        """
        Place new orders into market.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The number of place instructions
        :param str customer_ref: Optional parameter allowing the client to pass a unique string
        (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param str market_version: Optional parameter allowing the client to specify which
        version of the market the orders should be placed on
        :param str customer_strategy_ref: An optional reference customers can use to specify
        which strategy has sent the order
        :param bool async: An optional flag (not setting equates to false) which specifies if
        the orders should be placed asynchronously
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.PlaceOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'placeOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.PlaceOrders, elapsed_time, lightweight)

    def cancel_orders(self, market_id=None, instructions=None, customer_ref=None, session=None, lightweight=None):
        """
        Cancel all bets OR cancel all bets on a market OR fully or partially
        cancel particular orders on a market.

        :param str market_id: If marketId and betId aren't supplied all bets are cancelled
        :param list instructions: All instructions need to be on the same market
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.CancelOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'cancelOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.CancelOrders, elapsed_time, lightweight)

    def update_orders(self, market_id, instructions, customer_ref=None, session=None, lightweight=None):
        """
        Update non-exposure changing field.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The update instructions
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.UpdateOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'updateOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.UpdateOrders, elapsed_time, lightweight)

    def replace_orders(self, market_id, instructions, customer_ref=None, market_version=None,
                       async=None, session=None, lightweight=None):
        """
        This operation is logically a bulk cancel followed by a bulk place.
        The cancel is completed first then the new orders are placed.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The number of replace instructions.  The limit
        of replace instructions per request is 60
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param str market_version: Optional parameter allowing the client to specify
        which version of the market the orders should be placed on
        :param str async: An optional flag (not setting equates to false) which specifies
        if the orders should be replaced asynchronously
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.ReplaceOrders
        """
        params = clean_locals(locals())
        method = '%s%s' % (self.URI, 'replaceOrders')
        (response, elapsed_time) = self.request(method, params, session)
        return self.process_response(response, resources.ReplaceOrders, elapsed_time, lightweight)
