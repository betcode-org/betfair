

class BaseFilter:
    """Base Filter"""


class StreamingMarketFilter(BaseFilter):

    def __init__(self, market_ids=None, bsp_market=None, betting_types=None, event_type_ids=None, event_ids=None,
                 turn_in_play_enabled=None, market_types=None, venues=None, country_codes=None):
        self.market_ids = market_ids or []
        self.bsp_market = bsp_market
        self.betting_types = betting_types or []
        self.event_type_ids = event_type_ids or []
        self.event_ids = event_ids or []
        self.turn_in_play_enabled = turn_in_play_enabled
        self.market_types = market_types or []
        self.venues = venues or []
        self.country_codes = country_codes or []

    @property
    def serialise(self):
        return {
            'marketIds': self.market_ids,
            'bspMarket': self.bsp_market,
            'bettingTypes': self.betting_types,
            'eventTypeIds': self.event_type_ids,
            'eventIds': self.event_ids,
            'turnInPlayEnabled': self.turn_in_play_enabled,
            'marketTypes': self.market_types,
            'venues': self.venues,
            'countryCodes': self.country_codes,
        }


class StreamingMarketDataFilter(BaseFilter):

    def __init__(self, fields=None, ladder_levels=None):
        """
        fields: EX_BEST_OFFERS_DISP, EX_BEST_OFFERS, EX_ALL_OFFERS, EX_TRADED,
                EX_TRADED_VOL, EX_LTP, EX_MARKET_DEF, SP_TRADED, SP_PROJECTED
        ladder_levels: 1->10
        """
        self.fields = fields or []
        self.ladder_levels = ladder_levels

    @property
    def serialise(self):
        return {
            'fields': self.fields,
            'ladderLevels': self.ladder_levels
        }


def time_range(from_=None, to=None):  # todo datetime conversion
    """
    :param str from_:
    :param str to:

    :return: dict
    """
    args = locals()
    return {
        k.replace('_', ''): v for k, v in args.items()
    }


def market_filter(textQuery=None, eventTypeIds=None, eventIds=None, competitionIds=None, marketIds=None, venues=None,
                  bspOnly=None, turnInPlayEnabled=None, inPlayOnly=None, marketBettingTypes=None, marketCountries=None,
                  marketTypeCodes=None, marketStartTime=None, withOrders=None):
    """
    :param str textQuery: restrict markets by text associated with it, e.g name, event, comp.
    :param list eventTypeIds: filter market data to data pertaining to specific event_type ids.
    :param list eventIds: filter market data to data pertaining to specific event ids.
    :param list competitionIds: filter market data to data pertaining to specific competition ids.
    :param list marketIds: filter market data to data pertaining to specific marketIds.
    :param list venues: restrict markets by venue (only horse racing has venue at the moment)
    :param bool bspOnly: restriction on bsp, not supplied will return all.
    :param bool turnInPlayEnabled: restriction on whether market will turn in play or not, not supplied returns all.
    :param bool inPlayOnly: restriction to currently inplay, not supplied returns all.
    :param list marketBettingTypes: filter market data by market betting types.
    :param list marketCountries: filter market data by country codes.
    :param list marketTypeCodes: filter market data to match the type of market e.g. MATCH_ODDS.
    :param dict marketStartTime: filter market data by time at which it starts.
    :param str withOrders: filter market data by specified order status.

    :return: dict
    """
    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def price_data(sp_available=False, sp_traded=False, ex_best_offers=False, ex_all_offers=False, ex_traded=False):
    """
    Create PriceData filter list from all args passed as True.
    :param bool sp_available: Amount available for the BSP auction.
    :param bool sp_traded: Amount traded in the BSP auction.
    :param bool ex_best_offers: Only the best prices available for each runner, to requested price depth.
    :param bool ex_all_offers: trumps EX_BEST_OFFERS if both settings are present
    :param bool ex_traded: Amount traded on the exchange.

    :returns: string values of all args specified as True.
    :rtype: list
    """
    args = locals()
    return [
        k.upper() for k, v in args.items() if v is True
    ]


def ex_best_offers_overrides(bestPricesDepth=None, rollupModel=None, rollupLimit=None,
                             rollupLiabilityThreshold=None, rollupLiabilityFactor=None):
    """
    Create filter to specify whether to accumulate market volume info, how deep a book to return and rollup methods if
    accumulation is selected.
    :param int bestPricesDepth: The maximum number of prices to return on each side for each runner.
    :param str rollupModel: method to use to accumulate market orders.
    :param int rollupLimit: The volume limit to use when rolling up returned sizes. The exact definition of the limit
    depends on the rollupModel.
                        If no limit is provided it will use minimum stake
    :param float rollupLiabilityThreshold: Only applicable when rollupModel is MANAGED_LIABILITY. The rollup model
    switches from being stake based to liability based at the smallest lay price which is >= rollupLiabilityThreshold
    :param int rollupLiabilityFactor: Only applicable when rollupModel is MANAGED_LIABILITY. (rollupLiabilityFactor *
    rollupLimit) is the minimum liabilty the user is deemed to be comfortable with. After the rollupLiabilityThreshold
    price subsequent volumes will be rolled up to minimum value such that the liability >= the minimum liability.

    :returns: parameters for inclusion in market data requests.
    :rtype: dict
    """

    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def price_projection(priceData=price_data(), exBestOffersOverrides=ex_best_offers_overrides(), virtualise=True,
                     rolloverStakes=False):
    """
    Selection criteria of the returning price data.
    :param list priceData: PriceData filter to specify what market data we wish to receive.
    :param dict exBestOffersOverrides: define order book depth, rollup method.
    :param bool virtualise: whether to receive virtualised prices also.
    :param bool rolloverStakes: whether to accumulate volume at each price as sum of volume at that price and all better
    prices.

    :returns: price data criteria for market data.
    :rtype: dict
    """
    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def place_instruction(orderType, selectionId, side, handicap=None, limitOrder=None, limitOnCloseOrder=None,
                      marketOnCloseOrder=None, customerOrderRef=None):
    """
    Create order instructions to place an order at exchange.
    :param str orderType: define type of order to place.
    :param int selectionId: selection on which to place order
    :param float handicap: handicap if placing order on asianhandicap type market
    :param str side: side of order
    :param ? limitOrder: if orderType is a limitOrder structure details of the order.
    :param ? limitOnCloseOrder: if orderType is a limitOnCloseOrder structure details of the order.
    :param ? marketOnCloseOrder: if orderType is a marketOnCloseOrder structure details of the order.
    :param str customerOrderRef: an optional reference customers can set to identify instructions..

    :return: orders to place.
    :rtype: dict
    """

    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def limit_order(size, price, persistenceType, timeInForce=None, minFillSize=None, betTargetType=None,
                betTargetSize=None):
    """
    Create a limit order to send to exchange.
    :param float size: amount in account currency to be sent.
    :param float price: price at which the order is to be sent.
    :param str persistenceType: what happens to order at turn in play.
    :param str timeInForce: specify if it is FillOrKill/FillAndKill. This value takes precedence over any
    PersistenceType value chosen.
    :param float minFillSize: the minimum amount to be filled for FillAndKill.
    :param str betTargetType: Specify the type of Target, bet to certain backer profit or certain payout value.
                          Used to adjust to lower stakes if filled at better levels.
    :param float betTargetSize: Size of payout of profit to bet.

    :returns: Order information to place a limit order.
    :rtype: dict
    """
    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def limit_on_close_order(liability, price):
    """
    Create limit order for the closing auction.
    :param float liability: amount to bet.
    :param float price: price at which to bet

    :returns: Order information to place a limit on close order.
    :rtype: dict
    """
    return locals()


def market_on_close_order(liability):
    """
    Create market order to be placed in the closing auction.
    :param float liability: amount to bet.

    :returns: Order information to place a market on close order.
    :rtype: dict
    """
    return locals()


def cancel_instruction(betId, sizeReduction=None):
    """
    Instruction to fully or partially cancel an order (only applies to LIMIT orders)
    :param str betId: identifier of the bet to cancel.
    :param float sizeReduction: If supplied then this is a partial cancel.

    :returns: cancellation report detailing status, cancellation requested and actual cancellation details.
    :rtype: dict
    """
    args = locals()
    return {
        k: v for k, v in args.items() if v is not None
    }


def replace_instruction(betId, newPrice):
    """
    Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price.
    Original order will be cancelled and a new order placed at the new price for the remaining stake.
    :param str betId: Unique identifier for the bet
    :param float newPrice: The price to replace the bet at

    :returns: replace report detailing status, replace requested and actual replace details.
    :rtype: dict
    """
    return locals()


def update_instruction(betId, newPersistenceType):
    """
    Instruction to update LIMIT bet's persistence of an order that do not affect exposure
    :param str betId: Unique identifier for the bet
    :param str newPersistenceType: The new persistence type to update this bet to.

    :returns: update report detailing status, update requested and update details.
    :rtype: dict
    """
    return locals()
