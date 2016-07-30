import datetime

from .baseendpoint import BaseEndpoint
from .. import resources


class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)