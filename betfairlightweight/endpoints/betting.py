import datetime

from .baseendpoint import BaseEndpoint
from .. import resources


class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, params=None, session=None):
        """
        :rtype: list[resources.EventTypeResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, params=None, session=None):
        """
        :rtype: list[resources.CompetitionResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, params=None, session=None):
        """
        :rtype: list[resources.TimeRangeResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, params=None, session=None):
        """
        :rtype: list[resources.EventResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, params=None, session=None):
        """
        :rtype: list[resources.MarketTypeResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, params=None, session=None):
        """
        :rtype: list[resources.CountryResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, params=None, session=None):
        """
        :rtype: list[resources.VenueResult]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, params=None, session=None):
        """
        :rtype: list[resources.MarketCatalogue]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)

    def list_market_book(self, params=None, session=None):
        """
        :rtype: list[resources.MarketBook]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketBook')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketBook, date_time_sent)

    def list_current_orders(self, params=None, session=None):
        """
        :rtype: list[resources.CurrentOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrentOrders, date_time_sent)

    def list_cleared_orders(self, params=None, session=None):
        """
        :rtype: list[resources.ClearedOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listClearedOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ClearedOrders, date_time_sent)

    def list_market_profit_and_loss(self, params=None, session=None):
        """
        :rtype: list[resources.MarketProfitLoss]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketProfitLoss, date_time_sent)

    def place_orders(self, params=None, session=None):
        """
        :rtype: list[resources.PlaceOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'placeOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.PlaceOrders, date_time_sent)

    def cancel_orders(self, params=None, session=None):
        """
        :rtype: list[resources.CancelOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'cancelOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CancelOrders, date_time_sent)

    def update_orders(self, params=None, session=None):
        """
        :rtype: list[resources.UpdateOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'updateOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.UpdateOrders, date_time_sent)

    def replace_orders(self, params=None, session=None):
        """
        :rtype: list[resources.ReplaceOrders]
        """
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'replaceOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ReplaceOrders, date_time_sent)
