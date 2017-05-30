from .utils import to_camel_case


def streaming_market_filter(market_ids=None, bsp_market=None, betting_types=None, event_type_ids=None, event_ids=None,
                            turn_in_play_enabled=None, market_types=None, venues=None, country_codes=None):
    """
    :param list market_ids: filter market data to data pertaining to specific marketIds.
    :param list event_type_ids: filter market data to data pertaining to specific event_type ids.
    :param list event_ids: filter market data to data pertaining to specific event ids.
    :param bool turn_in_play_enabled: restriction on whether market will turn in play or not, not supplied returns all.
    :param list venues: restrict markets by venue (only horse racing has venue at the moment)
    :param bool bsp_market: restriction on bsp, not supplied will return all.
    :param list betting_types: filter on betting types
    :param list market_types: filter market data by market types.
    :param list country_codes: filter based on country codes

    :return: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def streaming_market_data_filter(fields=None, ladder_levels=None):
    """
    :param list fields: EX_BEST_OFFERS_DISP, EX_BEST_OFFERS, EX_ALL_OFFERS, EX_TRADED,
    EX_TRADED_VOL, EX_LTP, EX_MARKET_DEF, SP_TRADED, SP_PROJECTED
    :param int ladder_levels: 1->10

    :return: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def streaming_order_filter(include_overall_position=None, customer_strategy_refs=None,
                           partition_matched_by_strategy_ref=None):
    """
    :param bool include_overall_position: Returns overall / net position (OrderRunnerChange.mb / OrderRunnerChange.ml)
    :param list customer_strategy_refs: Restricts to specified customerStrategyRefs; this will filter orders and
    StrategyMatchChanges accordingly (Note: overall postition is not filtered)
    :param bool partition_matched_by_strategy_ref: Returns strategy positions (OrderRunnerChange.smc=
    Map<customerStrategyRef, StrategyMatchChange>) - these are sent in delta format as per overall position.

    :return: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
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


def market_filter(text_query=None, event_type_ids=None, event_ids=None, competition_ids=None, market_ids=None,
                  venues=None, bsp_only=None, turn_in_play_enabled=None, in_play_only=None, market_betting_types=None,
                  market_countries=None, market_type_codes=None, market_start_time=None, with_orders=None):
    """
    :param str text_query: restrict markets by text associated with it, e.g name, event, comp.
    :param list event_type_ids: filter market data to data pertaining to specific event_type ids.
    :param list event_ids: filter market data to data pertaining to specific event ids.
    :param list competition_ids: filter market data to data pertaining to specific competition ids.
    :param list market_ids: filter market data to data pertaining to specific marketIds.
    :param list venues: restrict markets by venue (only horse racing has venue at the moment)
    :param bool bsp_only: restriction on bsp, not supplied will return all.
    :param bool turn_in_play_enabled: restriction on whether market will turn in play or not, not supplied returns all.
    :param bool in_play_only: restriction to currently inplay, not supplied returns all.
    :param list market_betting_types: filter market data by market betting types.
    :param list market_countries: filter market data by country codes.
    :param list market_type_codes: filter market data to match the type of market e.g. MATCH_ODDS.
    :param dict market_start_time: filter market data by time at which it starts.
    :param str with_orders: filter market data by specified order status.

    :return: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
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


def ex_best_offers_overrides(best_prices_depth=None, rollup_model=None, rollup_limit=None,
                             rollup_liability_threshold=None, rollup_liability_factor=None):
    """
    Create filter to specify whether to accumulate market volume info, how deep a book to return and rollup methods if
    accumulation is selected.
    :param int best_prices_depth: The maximum number of prices to return on each side for each runner.
    :param str rollup_model: method to use to accumulate market orders.
    :param int rollup_limit: The volume limit to use when rolling up returned sizes. The exact definition of the limit
    depends on the rollupModel.
                        If no limit is provided it will use minimum stake
    :param float rollup_liability_threshold: Only applicable when rollupModel is MANAGED_LIABILITY. The rollup model
    switches from being stake based to liability based at the smallest lay price which is >= rollupLiabilityThreshold
    :param int rollup_liability_factor: Only applicable when rollupModel is MANAGED_LIABILITY. (rollupLiabilityFactor *
    rollupLimit) is the minimum liabilty the user is deemed to be comfortable with. After the rollupLiabilityThreshold
    price subsequent volumes will be rolled up to minimum value such that the liability >= the minimum liability.

    :returns: parameters for inclusion in market data requests.
    :rtype: dict
    """

    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def price_projection(price_data=price_data(), ex_best_offers_overrides=ex_best_offers_overrides(), virtualise=True,
                     rollover_stakes=False):
    """
    Selection criteria of the returning price data.
    :param list price_data: PriceData filter to specify what market data we wish to receive.
    :param dict ex_best_offers_overrides: define order book depth, rollup method.
    :param bool virtualise: whether to receive virtualised prices also.
    :param bool rollover_stakes: whether to accumulate volume at each price as sum of volume at that price and all better
    prices.

    :returns: price data criteria for market data.
    :rtype: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def place_instruction(order_type, selection_id, side, handicap=None, limit_order=None, limit_on_close_order=None,
                      market_on_close_order=None, customer_order_ref=None):
    """
    Create order instructions to place an order at exchange.
    :param str order_type: define type of order to place.
    :param int selection_id: selection on which to place order
    :param float handicap: handicap if placing order on asianhandicap type market
    :param str side: side of order
    :param resources.LimitOrder limit_order: if orderType is a limitOrder structure details of the order.
    :param resources.LimitOnCloseOrder limit_on_close_order: if orderType is a
    limitOnCloseOrder structure details of the order.
    :param resources.MarketOnCloseOrder market_on_close_order: if orderType is
    a marketOnCloseOrder structure details of the order.
    :param str customer_order_ref: an optional reference customers can set to identify instructions..

    :return: orders to place.
    :rtype: dict
    """

    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def limit_order(price, persistence_type=None, size=None, time_in_force=None, min_fill_size=None, bet_target_type=None,
                bet_target_size=None):
    """
    Create a limit order to send to exchange.
    :param float size: amount in account currency to be sent.
    :param float price: price at which the order is to be sent.
    :param str persistence_type: what happens to order at turn in play.
    :param str time_in_force: specify if it is FillOrKill/FillAndKill. This value takes precedence over any
    PersistenceType value chosen.
    :param float min_fill_size: the minimum amount to be filled for FillAndKill.
    :param str bet_target_type: Specify the type of Target, bet to certain backer profit or certain payout value.
                          Used to adjust to lower stakes if filled at better levels.
    :param float bet_target_size: Size of payout of profit to bet.

    :returns: Order information to place a limit order.
    :rtype: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
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


def cancel_instruction(bet_id, size_reduction=None):
    """
    Instruction to fully or partially cancel an order (only applies to LIMIT orders)
    :param str bet_id: identifier of the bet to cancel.
    :param float size_reduction: If supplied then this is a partial cancel.

    :returns: cancellation report detailing status, cancellation requested and actual cancellation details.
    :rtype: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def replace_instruction(bet_id, new_price):
    """
    Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price.
    Original order will be cancelled and a new order placed at the new price for the remaining stake.
    :param str bet_id: Unique identifier for the bet
    :param float new_price: The price to replace the bet at

    :returns: replace report detailing status, replace requested and actual replace details.
    :rtype: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }


def update_instruction(bet_id, new_persistence_type):
    """
    Instruction to update LIMIT bet's persistence of an order that do not affect exposure
    :param str bet_id: Unique identifier for the bet
    :param str new_persistence_type: The new persistence type to update this bet to.

    :returns: update report detailing status, update requested and update details.
    :rtype: dict
    """
    args = locals()
    return {
        to_camel_case(k): v for k, v in args.items() if v is not None
    }
