from .baseresource import BaseResource


class EventType(BaseResource):
    class Meta:
        identifier = 'event_type'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class EventTypeResult(BaseResource):
    class Meta:
        identifier = 'event_type_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'eventType': EventType
        }


class Competition(BaseResource):
    class Meta:
        identifier = 'competition'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class CompetitionResult(BaseResource):
    class Meta:
        identifier = 'competition_result'
        attributes = {
            'marketCount': 'market_count',
            'competitionRegion': 'competition_region'
        }
        sub_resources = {
            'competition': Competition
        }


class TimeRange(BaseResource):
    class Meta:
        identifier = 'time_range'
        attributes = {
            'from': '_from',
            'to': 'to'
        }


class TimeRangeResult(BaseResource):
    class Meta:
        identifier = 'time_range_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'timeRange': TimeRange
        }


class Event(BaseResource):
    class Meta:
        identifier = 'event'
        attributes = {
            'id': 'id',
            'openDate': 'open_date',
            'timezone': 'time_zone',
            'countryCode': 'country_code',
            'name': 'name',
            'venue': 'venue'
        }


class EventResult(BaseResource):
    class Meta:
        identifier = 'event_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'event': Event
        }


class MarketTypeResult(BaseResource):
    class Meta:
        identifier = 'market_type_result'
        attributes = {
            'marketCount': 'market_count',
            'marketType': 'market_type'
        }


class CountryResult(BaseResource):
    class Meta:
        identifier = 'country_result'
        attributes = {
            'marketCount': 'market_count',
            'countryCode': 'country_code'
        }


class VenueResult(BaseResource):
    class Meta:
        identifier = 'venue_result'
        attributes = {
            'marketCount': 'market_count',
            'venue': 'venue'
        }


class MarketCatalogueDescription(BaseResource):
    class Meta:
        identifier = 'description'
        attributes = {
            'bettingType': 'betting_type',
            'bspMarket': 'bsp_market',
            'discountAllowed': 'discount_allowed',
            'marketBaseRate': 'market_base_rate',
            'marketTime': 'market_time',
            'marketType': 'market_type',
            'persistenceEnabled': 'persistence_enabled',
            'regulator': 'regulator',
            'rules': 'rules',
            'rulesHasDate': 'rules_has_date',
            'suspendTime': 'suspend_time',
            'turnInPlayEnabled': 'turn_in_play_enabled',
            'wallet': 'wallet'
        }


class MarketCatalogue(BaseResource):
    class Meta:
        identifier = 'market_catalogue'
        attributes = {
            'marketId': 'market_id',
            'marketName': 'market_name',
            'totalMatched': 'total_matched',
            'marketStartTime': 'market_start_time'
        }
        sub_resources = {
            'competition': Competition,
            'event': Event,
            'eventType': EventType,
            'description': MarketCatalogueDescription,
            # 'runners': None
        }
