import unittest
import datetime

from betfairlightweight import resources

from tests.tools import create_mock_json


class BettingResourcesTest(unittest.TestCase):

    DATE_TIME_SENT = datetime.datetime(2003, 8, 4, 12, 30, 45)

    def test_event_type_result(self):
        mock_response = create_mock_json('tests/resources/list_event_types.json')
        event_types = mock_response.json().get('result')

        for event_type in event_types:
            resource = resources.EventTypeResult(date_time_sent=self.DATE_TIME_SENT,
                                                 **event_type)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == event_type['marketCount']
            assert resource.event_type.id == event_type['eventType']['id']
            assert resource.event_type.name == event_type['eventType']['name']

    def test_competition_result(self):
        mock_response = create_mock_json('tests/resources/list_competitions.json')
        competitions = mock_response.json().get('result')

        for competition in competitions:
            resource = resources.CompetitionResult(date_time_sent=self.DATE_TIME_SENT,
                                                   **competition)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == competition['marketCount']
            assert resource.competition_region == competition['competitionRegion']
            assert resource.competition.id == competition['competition']['id']
            assert resource.competition.name == competition['competition']['name']

    def test_time_range_result(self):
        mock_response = create_mock_json('tests/resources/list_time_ranges.json')
        time_ranges = mock_response.json().get('result')

        for time_range in time_ranges:
            resource = resources.TimeRangeResult(date_time_sent=self.DATE_TIME_SENT,
                                                 **time_range)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == time_range['marketCount']
            assert resource.time_range._from == time_range['timeRange']['from']
            assert resource.time_range.to == time_range['timeRange']['to']

    def test_event_result(self):
        mock_response = create_mock_json('tests/resources/list_events.json')
        event_results = mock_response.json().get('result')

        for event_result in event_results:
            resource = resources.EventResult(date_time_sent=self.DATE_TIME_SENT,
                                             **event_result)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == event_result['marketCount']
            assert resource.event.id == event_result['event']['id']
            assert resource.event.open_date == event_result['event']['openDate']
            assert resource.event.time_zone == event_result['event']['timezone']
            assert resource.event.country_code == event_result['event']['countryCode']
            assert resource.event.name == event_result['event']['name']
            assert resource.event.venue == event_result['event']['venue']

    def test_market_type_result(self):
        mock_response = create_mock_json('tests/resources/list_market_types.json')
        market_type_results = mock_response.json().get('result')

        for market_type_result in market_type_results:
            resource = resources.MarketTypeResult(date_time_sent=self.DATE_TIME_SENT,
                                                  **market_type_result)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == market_type_result['marketCount']
            assert resource.market_type == market_type_result['marketType']

    def test_country_result(self):
        mock_response = create_mock_json('tests/resources/list_countries.json')
        countries_results = mock_response.json().get('result')

        for countries_result in countries_results:
            resource = resources.CountryResult(date_time_sent=self.DATE_TIME_SENT,
                                               **countries_result)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == countries_result['marketCount']
            assert resource.country_code == countries_result['countryCode']

    def test_venue_result(self):
        mock_response = create_mock_json('tests/resources/list_venues.json')
        venue_results = mock_response.json().get('result')

        for venue_result in venue_results:
            resource = resources.VenueResult(date_time_sent=self.DATE_TIME_SENT,
                                             **venue_result)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_count == venue_result['marketCount']
            assert resource.venue == venue_result['venue']

    def test_market_catalogue(self):
        mock_response = create_mock_json('tests/resources/list_market_catalogue.json')
        market_catalogues = mock_response.json().get('result')

        for market_catalogue in market_catalogues:
            resource = resources.MarketCatalogue(date_time_sent=self.DATE_TIME_SENT,
                                                 **market_catalogue)

            assert resource.datetime_sent == self.DATE_TIME_SENT
            assert resource.market_id == market_catalogue['marketId']
            assert resource.market_name == market_catalogue['marketName']
            assert resource.total_matched == market_catalogue['totalMatched']
            assert resource.market_start_time == market_catalogue['marketStartTime']

            assert resource.competition.id == market_catalogue['competition']['id']
            assert resource.competition.name == market_catalogue['competition']['name']

            assert resource.event.id == market_catalogue['event']['id']
            assert resource.event.open_date == market_catalogue['event']['openDate']
            assert resource.event.time_zone == market_catalogue['event']['timezone']
            assert resource.event.country_code == market_catalogue['event']['countryCode']
            assert resource.event.name == market_catalogue['event']['name']
            assert resource.event.venue == market_catalogue['event'].get('venue')

            assert resource.event_type.id == market_catalogue['eventType']['id']
            assert resource.event_type.name == market_catalogue['eventType']['name']

            assert resource.description.betting_type == market_catalogue['description']['bettingType']
            assert resource.description.bsp_market == market_catalogue['description']['bspMarket']
            assert resource.description.discount_allowed == market_catalogue['description']['discountAllowed']
            assert resource.description.market_base_rate == market_catalogue['description']['marketBaseRate']
            assert resource.description.market_time == market_catalogue['description']['marketTime']
            assert resource.description.market_type == market_catalogue['description']['marketType']
            assert resource.description.persistence_enabled == market_catalogue['description']['persistenceEnabled']
            assert resource.description.regulator == market_catalogue['description']['regulator']
            assert resource.description.rules == market_catalogue['description']['rules']
            assert resource.description.rules_has_date == market_catalogue['description']['rulesHasDate']
            assert resource.description.suspend_time == market_catalogue['description']['suspendTime']
            assert resource.description.turn_in_play_enabled == market_catalogue['description']['turnInPlayEnabled']
            assert resource.description.wallet == market_catalogue['description']['wallet']