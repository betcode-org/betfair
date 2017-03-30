

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
