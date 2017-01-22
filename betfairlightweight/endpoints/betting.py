import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..filters import (MarketFilter, MarketProjection, PriceProjection)
from ..enums import (TimeGranularity, MarketSort, OrderProjection, MatchProjection, SortDir, OrderBy, BetStatus)
from ..utils import clean_locals

class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get breakdown of market counts by sport associated with specified MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: language used for response
        :type locale: str
        :returns: sports names, sportsIds and market counts.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get breakdown of market counts by competitions associated with a given market filter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: language used for response
        :type locale: str
        :returns: competitions info and market counts.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, session=None, granularity=TimeGranularity.Days, filter=MarketFilter()):
        """
        Get breakdown of market counts grouped by specified time granularity.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param granularity: granularity at which to breakdown the market counts.
        :type granularity: BetfairAPI.bin.utils.TimeGranularity
        :returns: market counts grouped by granularity.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get breakdown of all events associated with a given MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: language used for response
        :type locale: str
        :returns: all event information.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get dataframe markets types associated with a given MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: language used for response
        :type locale: str
        :returns: market counts grouped by marketType.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get breakdown of all market counts by country for given MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: language used for response
        :type locale: str
        :returns: Market counts grouped by countryCode.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, session=None, filter=MarketFilter(), locale=None):
        """
        Get breakdown of all venue information associated with a given MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param locale: Language used for response
        :type locale: str
        :returns: Market count grouped by venue.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, session=None, filter=MarketFilter(), maxResults=1000, marketProjection=MarketProjection(),
                              locale=None, sort=MarketSort.FirstStart):
        """
        Get breakdown of all market information associated with a given MarketFilter.

        :param filter: MarketFilter to filter selected markets.
        :type filter: BetfairAPI.bin.utils.MarketFilter
        :param maxResults: number of results to show, max 1000.
        :type maxResults: int
        :param marketProjection: list of data to be included in the catalogue returned.
        :type marketProjection: BetfairAPI.bin.utils.MarketProjection
        :param locale: language used for response
        :type locale: str
        :param sort: MarketSort method to sort the results. If none Betfair rank is used.
        :type sort: BetfairAPI.bin.enums.MarketSort
        :returns: market data.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)

    def list_market_book(self, marketIds, session=None, depth=3, priceProjection=PriceProjection(),
                         orderProjection=OrderProjection.Executable, matchProjection=MatchProjection.NoRoll,
                         currencyCode=None, locale=None):
        """
        Get the order book and traded data for specified marketIds.

        :param marketIds: List of market ID strings.
        :type marketIds: list
        :param depth: number of back and offers to be displayed
        :type depth: int
        :param priceProjection: dictionary of price settings.
        :type priceProjection: BetfairAPI.bin.utils.PriceProjection
        :param orderProjection: orders to be included in response.
        :type orderProjection: BetfairAPI.bin.enums.OrderProjection
        :param matchProjection: settings for order volume data to be returned.
        :type matchProjection: BetfairAPI.bin.enums.MatchProjection
        :param currencyCode: currency used, if none provided account default is used.
        :type currencyCode: str
        :param locale: language used for response, if none provided account default is used.
        :type locale: str
        :returns: order book data and traded data for each runner in each specified marketId
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketBook')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketBook, date_time_sent)

    def list_current_orders(self, session=None, betIds=None, marketIds=None, orderProjection=OrderProjection.All,
                            dateRange=None, orderBy=OrderBy.PlaceTime, sortDir=SortDir.TimeAscending,
                            fromRecord=0, toRecord=0):
        """
        Get all current orders filtered by specified arguments.

        :param betIds: List of bet id strings to restrict order on. max 250 ids
        :type betIds: list
        :param marketIds: List of market id strings to restrict order on. max 250 ids
        :type marketIds: list
        :param orderProjection: Type of orders to include in results.
        :type orderProjection: BetfairAPI.bin.enums.OrderProjection
        :param dateRange: TimeRange (inclusive) to restrict orders.
        :type dateRange: BetfairAPI.bin.utils.create_timerange
        :param orderBy: Specify how orders returned are ordered.
        :type orderBy: BetfairAPI.bin.enums.OrderType
        :param sortDir: direction in which results are sported.
        :type sortDir: BetfairAPI.bin.enums.SortDir
        :param fromRecord: starting record to return.
        :type fromRecord: int
        :param toRecord: record to stop at, value 0 means return all up to limit. limit 1000
        :type toRecord: int
        :return: current order information.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrentOrders, date_time_sent)

    def list_cleared_orders(self, session=None, betStatus=BetStatus.Settled, eventTypeIds=None, eventIds=None, marketIds=None,
                            runnerIds=None, betIds=None, side=None, settledDateRange=None, groupBy=None,
                            includeItemDescription=True, locale=None, fromRecord=0, toRecord=0):
        """
        Get all cleared orders filtered by specified arguments.

        :param betStatus: restrict results by specific bet status.
        :type betStatus: BetfairAPI.bin.enums.BetStatus
        :param eventTypeIds: restrict results by eventTypeIds.
        :type eventTypeIds: list
        :param eventIds: restrict results by eventIds.
        :type eventIds: list
        :param marketIds: restrict results by marketIds.
        :type marketIds: list
        :param runnerIds: restrict results by runnerIds.
        :type runnerIds: list
        :param betIds: restrict results by betIds.
        :type betIds: list
        :param side: restrict results by side.
        :type side: BetfairAPI.bin.enums.Side
        :param settledDateRange: restrict settlement dates to include.
        :type settledDateRange: BetfairAPI.bin.utils.create_timerange
        :param groupBy: aggregation method for Settled betStatus.
        :type groupBy: BetfairAPI.bin.enums.GroupBy
        :param includeItemDescription: boolean to include item description or not.
        :type includeItemDescription: bool
        :param locale: language to return data in.
        :type locale: str
        :param fromRecord: starting record to return.
        :type fromRecord: int
        :param toRecord: record to stop at, value 0 means return all up to limit. limit 1000.
        :type toRecord: int
        :returns: All cleared orders for specified filter parameters.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listClearedOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ClearedOrders, date_time_sent)

    def list_market_profit_and_loss(self, marketIds, session=None, includeSettledBets=False, includeBspBets=None,
                                    netOfCommission=None):
        """
        Get profit and loss for a given list of markets.

        :param marketIds: markets to calculate profit and loss.
        :type marketIds: list
        :param includeSettledBets: Option to include settled bets.
        :type includeSettledBets: bool
        :param includeBspBets: Option to include BSP bets.
        :type includeBspBets: bool
        :param netOfCommission: Option to return profit and loss net of users current commission rate and special tariffs.
        :type netOfCommission: bool
        :returns: profit and lost grouped by marketId.
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketProfitLoss, date_time_sent)

    def place_orders(self, marketId, OrderList, session=None, customerRef=None, marketVersion=None):
        """
        Place orders at exchange.


        :param marketId: id of the market on which the orders are to be placed.
        :type marketId: str
        :param OrderList: list of PlaceInstructions instances which define information to create each order.
        :type OrderList: BetfairAPI.bin.utils.PlaceInstructions
        :param customerRef: unique string (up to 32 chars) that is used to de-dupe mistaken re-submissions.
        :type customerRef: str
        :param marketVersion: optional parameter of market state into which to place orders,
                              if states don't match orders will lapse.
        :type marketVersion: int
        :returns: report of order status, matched, remaining and average price.
        """
        if not isinstance(OrderList, list):
            raise ValueError('Orders placement must be supplied as a list of PlaceInstructions dictionaries.')
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'placeOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.PlaceOrders, date_time_sent)

    def cancel_orders(self, session=None, marketId=None, instructions=None, customerRef=None):
        """
        Cancel or reduce orders currently at exchange.

        :param marketId: id of the market as string on which the orders are to be cancelled.
        :type marketId: str
        :param instructions: list of dictionaries which contain betId and sizeReduction for each order. max 60.
        :type instructions: BetfairAPI.bin.utils.CancelInfo
        :param customerRef: unique string (up to 32 chars) that is used to de-dupe mistaken re-submissions.
        :type customerRef: str
        :returns: cancellation report confirming adjustments to all bets.

        .. note:: if no marketId or BetInfo is supplied all bets are cancelled.
        .. note:: if only a marketId is passed all bets on that market are cancelled.

        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'cancelOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CancelOrders, date_time_sent)

    def update_orders(self, session=None, marketId=None, instructions=None, customerRef=None):
        """
        Update non exposure changing fields of orders at exchange.

        :param marketId: id of the market as string on which the orders are to be updated.
        :type marketId: str
        :param instructions: list of dictionaries which contain betId and newPersistenceType for each order. max 60.
        :type instructions: BetfairAPI.bin.utils.UpdateInfo
        :param customerRef: unique string (up to 32 chars) that is used to de-dupe mistaken re-submissions.
        :type customerRef: str
        :returns: report of updated orders data.
        """
        if not isinstance(instructions, list):
            raise ValueError('Order amends must be supplied as a list of UpdateInfo dictionaries.')
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'updateOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.UpdateOrders, date_time_sent)

    def replace_orders(self, session=None, marketId=None, instructions=None, customerRef=None):
        """
        Change the price of orders at exchange.

        :param marketId: id of the market as string on which the orders are to be replaced.
        :type marketId: str
        :param instructions: list of dictionaries which contain betId and newPrice for each order. max 60.
        :type instructions: BetfairAPI.bin.utils.ReplaceInfo
        :param customerRef: unique string (up to 32 chars) that is used to de-dupe mistaken re-submissions.
        :type customerRef: str
        :returns: report of order status, matched, remaining and average price.
        """
        if not isinstance(instructions, list):
            raise ValueError('Order price amends must be supplied as a list of ReplaceInfo dictionaries.')
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'replaceOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ReplaceOrders, date_time_sent)
