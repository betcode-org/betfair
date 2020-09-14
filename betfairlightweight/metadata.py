"""
Useful metadata/limits from:
    https://developer.betfair.com/exchange-api/
"""

transaction_limit = 5000  # transactions per hour (£0.002 cost per transaction after)


order_limits = {
    "placeOrders": 200,
    "cancelOrders": 60,
    "updateOrders": 60,
    "replaceOrders": 60,
}

list_current_orders = {"marketIds": 250, "orders": 1000}


"""
Market Data Request Limits
    The following tables explain the "weighting" of data for each MarketProjection or PriceProjection.
    If you exceed the maximum weighting of 200 points, the API will return a TOO_MUCH_DATA error

    Please note: specific combinations of priceProjections will carry different weights that aren't the sum of
    their individual weights. Please see a summary of these below:

    PriceProjection	Weight
        EX_BEST_OFFERS + EX_TRADED	20
        EX_ALL_OFFERS + EX_TRADED   32

    If exBestOffersOverrides is used the weight is calculated by weight * (requestedDepth/3).
"""

list_market_catalogue = {
    "MARKET_DESCRIPTION": 1,
    "RUNNER_DESCRIPTION": 0,
    "EVENT": 0,
    "EVENT_TYPE": 0,
    "COMPETITION": 0,
    "RUNNER_METADATA": 1,
    "MARKET_START_TIME": 0,
}

list_market_book = {
    "": 2,
    "SP_AVAILABLE": 3,
    "EX_BEST_OFFERS": 5,
    "SP_TRADED": 7,
    "EX_ALL_OFFERS": 17,
    "EX_TRADED": 17,
}

list_market_profit_and_loss = {"": 4}


"""
Currency Parameters
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information#AdditionalInformation-CurrencyParameters
"""

currency_parameters = {
    "GBP": {"min_bet_size": 2, "min_bet_payout": 10, "min_bsp_liability": 10},
    "EUR": {"min_bet_size": 2, "min_bet_payout": 20, "min_bsp_liability": 20},
    "USD": {"min_bet_size": 3, "min_bet_payout": 20, "min_bsp_liability": 20},
    "HKD": {"min_bet_size": 25, "min_bet_payout": 125, "min_bsp_liability": 125},
    "AUD": {"min_bet_size": 5, "min_bet_payout": 30, "min_bsp_liability": 30},
    "CAD": {"min_bet_size": 6, "min_bet_payout": 30, "min_bsp_liability": 30},
    "DKK": {"min_bet_size": 30, "min_bet_payout": 150, "min_bsp_liability": 150},
    "NOK": {"min_bet_size": 30, "min_bet_payout": 150, "min_bsp_liability": 150},
    "SEK": {"min_bet_size": 30, "min_bet_payout": 150, "min_bsp_liability": 150},
    "SGD": {"min_bet_size": 6, "min_bet_payout": 30, "min_bsp_liability": 30},
    "RON": {"min_bet_size": 10, "min_bet_payout": 50, "min_bsp_liability": 50},
    "BRL": {"min_bet_size": 10, "min_bet_payout": 50, "min_bsp_liability": 50},
}
