from enums import *

class BaseFilter:
    ''''''


def StreamingDataFields(EX_BEST_OFFERS_DISP=False, EX_BEST_OFFERS=False, EX_ALL_OFFERS=True, EX_TRADED=True,
                        EX_TRADED_VOL=False, EX_LTP=False, EX_MARKET_DEF=True, SP_TRADED=False, SP_PROJECTED=False):
    """
    Create PriceData filter list from all args passed as True.

    :param EX_BEST_OFFERS_DISP: Best prices including virtual prices - depth is controlled by ladderLevels (1 to 10).
                                Data fields returned: bdatb, bdatl. Data format returned: level, price, size.
    :param EX_BEST_OFFERS: Best prices not including virtual prices - depth is controlled by ladderLevels (1 to 10).
                           Data fields returned: batb, batl. Data format returned: level, price, size.
    :param EX_ALL_OFFERS: Full available to BACK/LAY ladder.
                          Data fields returned: atb, atl. Data format returned: price, size.
    :param EX_TRADED: Full traded ladder.
                      Data fields returned: trd. Data format returned: price, size.
    :param EX_TRADED_VOL: Market and runner level traded volume.
                          Data fields returned: tv. Data format returned: size.
    :param EX_LTP: Last traded price.
                   Data fields returned: ltp. Data format returned: price.
    :param EX_MARKET_DEF: Send market definitions.
                          Data fields returned: marketDefinition. Data format returned: MarketDefinition.
    :param SP_TRADED: Starting price ladder.
                      Data fields returned: spb, spl. Data format returned: price, size.
    :param SP_PROJECTED: Starting price projection prices.
                      Data fields returned: spn, spf. Data format returned: price.
    :returns: string values of all args specified as True.
    :rtype: list
    """
    args = locals()
    return [k for k, v in args.iteritems() if v is True]


def StreamingMarketFilter(market_ids=None, bsp_market=None, betting_types=None, event_type_ids=None, event_ids=None,
                 turn_in_play_enabled=None, market_types=None, venues=None, country_codes=None):
    args = {
        'marketIds': market_ids,
        'bspMarket': bsp_market,
        'bettingTypes': betting_types,
        'eventTypeIds': event_type_ids,
        'eventIds': event_ids,
        'turnInPlayEnabled': turn_in_play_enabled,
        'marketTypes': market_types,
        'venues': venues,
        'countryCodes': country_codes,
    }
    filters = dict((k, v) for k, v in args.iteritems() if v is not None)
    return filters


def StreamingMarketDataFilter(fields=StreamingDataFields(), ladder_levels=3):
    """
    Filter the level of detail to subscribe to in streaming.

    :param fields: Data fields to subscribe to.
    :type fields: StreamingDataFields
    :param ladder_levels: the depth of ladder information to include.
    :type ladder_levels: int(1-10)
    """
    return {
        'fields': fields,
        'ladderLevels': ladder_levels
    }


def StreamingOrderDataFilter(includeOverallPosition=True, customerStrategyRefs=None, partitionMatchedByStrategyRef=False):
    """
    Filter the orders to which a stream subscribes.

    :param includeOverallPosition: Returns overall / net position (OrderRunnerChange.mb / OrderRunnerChange.ml).
    :type includeOverallPosition: bool
    :param customerStrategyRefs: Restricts to specified customerStrategyRefs; this will filter orders and
                                 StrategyMatchChanges accordingly (Note: overall postition is not filtered)
    :type customerStrategyRefs: list of strings
    :param partitionMatchedByStrategyRef: Returns strategy positions (OrderRunnerChange.smc=Map<customerStrategyRef, StrategyMatchChange>)
                                          - these are sent in delta format as per overall position.
    :type partitionMatchedByStrategyRef: bool
    :return: dictionary containing filter information.

    """
    filters = dict((k, v) for k, v in locals().iteritems() if v is not None)
    return filters


def MarketFilter(textQuery=None, exchangeIds=None, eventTypeIds=None, eventIds=None, competitionIds=None,
                 marketIds=None, venues=None, bspOnly=None, turnInPlayEnabled=None, inPlayOnly=None,
                 marketBettingTypes=None, marketCountries=None, marketTypeCodes=None, marketStartTime=None,
                 withOrders=None):
    """
    Create filters to apply to market data we wish to receive.

    :param textQuery: restrict markets by text associated with it, e.g name, event, comp.
    :type textQuery: str
    :param exchangeIds: filter market data to data pertaining to specific exchange ids.
    :type exchangeIds: list
    :param eventTypeIds: filter market data to data pertaining to specific event_type ids.
    :type eventIds: list
    :param eventIds: filter market data to data pertaining to specific event ids.
    :type eventTypeIds: list
    :param competitionIds: filter market data to data pertaining to specific competition ids.
    :type competitionIds: list
    :param marketIds: filter market data to data pertaining to specific marketIds.
    :type marketIds: list
    :param venues: restrict markets by venue (only horse racing has venue at the moment)
    :type venues: list
    :param bspOnly: restriction on bsp, not supplied will return all.
    :type bspOnly: bool
    :param turnInPlayEnabled: restriction on whether market will turn in play or not, not supplied returns all.
    :type turnInPlayEnabled: bool
    :param inPlayOnly: restriction to currently inplay, not supplied returns all.
    :type inPlayOnly: bool
    :param marketBettingTypes: filter market data by market betting types.
    :type marketBettingTypes: list
    :param marketCountries: filter market data by country codes.
    :type marketCountries: list
    :param marketTypeCodes: filter market data to match the type of market e.g. MATCH_ODDS.
    :type marketTypeCodes: list
    :param marketStartTime: filter market data by time at which it starts.
    :type marketStartTime: BetfairAPI.bin.utils.create_timerange
    :param withOrders: filter market data by specified order status.
    :type withOrders: BetfairAPI.bin.enums.OrderStatus
    :returns: filter dictionary to be applied to market data request.
    :rtype: dict
    """
    args = locals()
    filters = dict((k, v) for k, v in args.iteritems() if v is not None)
    return filters


def MarketProjection(COMPETITION=True, MARKET_DESCRIPTION=True, EVENT=True, EVENT_TYPE=True, RUNNER_METADATA=False,
                     RUNNER_DESCRIPTION=True, MARKET_START_TIME=True):
    """
    Create MarketProjection filter list from all args passed as True.

    :param COMPETITION: If not selected then the competition will not be returned with marketCatalogue.
    :type COMPETITION: bool
    :param MARKET_DESCRIPTION: If not selected then the description will not be returned with marketCatalogue.
    :type MARKET_DESCRIPTION: bool
    :param EVENT: If not selected then the event will not be returned with marketCatalogue.
    :type EVENT: bool
    :param EVENT_TYPE: If not selected then the eventType will not be returned with marketCatalogue.
    :type EVENT_TYPE: bool
    :param RUNNER_METADATA: If not selected then the runner metadata will not be returned with marketCatalogue.
                            If selected then RUNNER_DESCRIPTION will also be returned regardless of whether
                            it is included as a market projection.
    :type RUNNER_METADATA: bool
    :param RUNNER_DESCRIPTION: If not selected then the runners will not be returned with marketCatalogue.
    :type RUNNER_DESCRIPTION: bool
    :param MARKET_START_TIME: If not selected then the start time will not be returned with marketCatalogue.
    :type MARKET_START_TIME: bool
    :returns: string values of all args specified as True.
    :rtype: list

    """
    args = locals()
    return [k for k, v in args.iteritems() if v is True]



def PriceData(SP_AVAILABLE=False, SP_TRADED=False, EX_BEST_OFFERS=True, EX_ALL_OFFERS=False, EX_TRADED=True):
    """
    Create PriceData filter list from all args passed as True.

    :param SP_AVAILABLE: Amount available for the BSP auction.
    :param SP_TRADED: Amount traded in the BSP auction.
    :param EX_BEST_OFFERS: Only the best prices available for each runner, to requested price depth.
    :param EX_ALL_OFFERS: trumps EX_BEST_OFFERS if both settings are present
    :param EX_TRADED: Amount traded on the exchange.
    :returns: string values of all args specified as True.
    :rtype: list
    """
    args = locals()
    return [k for k, v in args.iteritems() if v is True]


def ExBestOffersOverrides(bestPricesDepth=3, rollupModel=RollUpModel.NoRoll, rollupLimit=None,
                          rollupLiabilityThreshold=None, rollupLiabilityFactor=None):
    """
    Create filter to specify whether to accumulate market volume info, how deep a book to return and rollup methods if accumulation is selected.

    :param bestPricesDepth: The maximum number of prices to return on each side for each runner.
    :type bestPricesDepth: int
    :param rollupModel: method to use to accumulate market orders.
    :type rollupModel: BetfairAPI.bin.enums.RollUpModel
    :param rollupLimit: The volume limit to use when rolling up returned sizes. The exact definition of the limit depends on the rollupModel.
                        If no limit is provided it will use minimum stake
    :type rollupLimit: int
    :param rollupLiabilityThreshold: Only applicable when rollupModel is MANAGED_LIABILITY. The rollup model switches from
                                     being stake based to liability based at the smallest lay price which is >= rollupLiabilityThreshold
    :type rollupLiabilityThreshold: float
    :param rollupLiabilityFactor: Only applicable when rollupModel is MANAGED_LIABILITY. (rollupLiabilityFactor * rollupLimit) is the
                                  minimum liabilty the user is deemed to be comfortable with.
                                  After the rollupLiabilityThreshold price subsequent volumes will be rolled up to minimum value such
                                  that the liability >= the minimum liability.
    :type rollupLiabilityFactor: int

    :returns: parameters for inclusion in market data requests.
    :rtype: dict

    """

    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def PriceProjection(priceData=PriceData(), exBestOffersOverrides=ExBestOffersOverrides(),
                    virtualise="true",
                    rolloverStakes="false"):
    """
    Selection criteria of the returning price data.

    :param priceData: PriceData filter to specify what market data we wish to receive.
    :type priceData: BetfairAPI.bin.utils.PriceData
    :param exBestOffersOverrides: define order book depth, rollup method.
    :type exBestOffersOverrides: BetfairAPI.bin.utils.ExBestOffersOverrides
    :param virtualise: whether to receive virtualised prices also.
    :type virtualise: bool
    :param rolloverStakes: whether to accumulate volume at each price as sum of volume at that price and all better prices.
    :type rolloverStakes: bool
    :returns: price data criteria for market data.
    :rtype: dict
    """
    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def PlaceInstructions(orderType=OrderType.LimitOrder, selectionId=None, handicap=None, side=None, limitOrder=None,
                      limitOnCloseOrder=None, marketOnCloseOrder=None):
    """
    Create order instructions to place an order at exchange.

    :param orderType: define type of order to place.
    :type orderType: BetfairAPI.bin.enums.OrderType
    :param selectionId: selection on which to place order
    :type selectionId: int
    :param handicap: handicap if placing order on asianhandicap type market
    :type handicap: float
    :param side: side of order
    :type side: BetfairAPI.bin.enums.Side
    :param limitOrder: if orderType is a limitOrder structure details of the order.
    :type limitOrder: BetfairAPI.bin.utils.LimitOrder
    :param limitOnCloseOrder: if orderType is a limitOnCloseOrder structure details of the order.
    :type LimitOnCloseOrder: BetfairAPI.bin.utils.LimitOnCloseOrder
    :param marketOnCloseOrder: if orderType is a marketOnCloseOrder structure details of the order.
    :type MarketOnCloseOrder: BetfairAPI.bin.utils.MarketOnCloseOrder
    :return: orders to place.
    :rtype: dict
    """

    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def LimitOrder(size=None, price=None, persistenceType=PersistenceType.Kill, timeInForce=None, minFillSize=None,
               betTargetType=None, betTargetSize=None):
    """
    Create a limit order to send to exchange.

    :param size: amount in account currency to be sent.
    :type size: float
    :param price: price at which the order is to be sent.
    :type price: float
    :param persistenceType: what happens to order at turn in play.
    :type persistenceType: BetfairAPI.bin.enums.PersistenceType
    :param timeInForce: specify if it is FillOrKill/FillAndKill. This value takes precedence over any PersistenceType value chosen.
    :type timeInForce: BetfairAPI.bin.enums.TimeInForce.
    :param minFillSize: the minimum amount to be filled for FillAndKill.
    :type minFillSize: float
    :param betTargetType: Specify the type of Target, bet to certain backer profit or certain payout value.
                          Used to adjust to lower stakes if filled at better levels.
    :type betTargetType: BetfairAPI.bin.enums.BetTargetType
    :param betTargetSize: Size of payout of profit to bet.
    :type betTargetSize: float
    :returns: Order information to place a limit order.
    :rtype: dict
    """
    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def LimitOnCloseOrder(liability=None, price=None):
    """
    Create limit order for the closing auction.

    :param liability: amount to bet.
    :type liability: float
    :param price: price at which to bet
    :type price: float
    :returns: Order information to place a limit on close order.
    :rtype: dict

    """
    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def MarketOnCloseOrder(liability=None):
    """
    Create market order to be placed in the closing auction.

    :param liability: amount to bet.
    :type liability: float
    :returns: Order information to place a market on close order.
    :rtype: dict

    """
    args = locals()
    return dict((k, v) for k, v in args.iteritems() if v is not None)


def CancelInfo(betId=None, sizeReduction=None):
    """
    Instruction to fully or partially cancel an order (only applies to LIMIT orders)

    :param betId: identifier of the bet to cancel.
    :type betId: str
    :param sizeReduction: If supplied then this is a partial cancel.
    :type sizeReduction: float
    :returns: cancellation report detailing status, cancellation requested and actual cancellation details.
    :rtype: Dataframe

    """
    return locals()


def ReplaceInfo(betId=None, newPrice=None):
    """
    Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price.
    Original order will be cancelled and a new order placed at the new price for the remaining stake.

    :param betId: Unique identifier for the bet
    :type betId: str
    :param newPrice: The price to replace the bet at
    :type newPrice: float
    :returns: replace report detailing status, replace requested and actual replace details.
    :rtype: Dataframe

    """
    return locals()


def UpdateInfo(betId=None, newPersistenceType=None):
    """
    Instruction to update LIMIT bet's persistence of an order that do not affect exposure

    :param betId: Unique identifier for the bet
    :type betId: str
    :param newPersistenceType: The new persistence type to update this bet to.
    :type newPersistenceType: BetfairAPI.bin.enums.PersistenceType
    :returns: update report detailing status, update requested and update details.
    :rtype: Dataframe

    """
    return locals()