import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..exceptions import TransactionCountError


class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def __init__(self, parent):
        super(Betting, self).__init__(parent)
        self._next_hour = None
        self.set_next_hour()
        self.transaction_count = 0
        self.transaction_limit = 999

    def list_event_types(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventTypeResult, date_time_sent)

    def list_competitions(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCompetitions')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CompetitionResult, date_time_sent)

    def list_time_ranges(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listTimeRanges')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.TimeRangeResult, date_time_sent)

    def list_events(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.EventResult, date_time_sent)

    def list_market_types(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketTypes')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketTypeResult, date_time_sent)

    def list_countries(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCountries')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CountryResult, date_time_sent)

    def list_venues(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listVenues')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.VenueResult, date_time_sent)

    def list_market_catalogue(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketCatalogue')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketCatalogue, date_time_sent)

    def list_market_book(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketBook')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketBook, date_time_sent)

    def list_current_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listCurrentOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CurrentOrders, date_time_sent)

    def list_cleared_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listClearedOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ClearedOrders, date_time_sent)

    def list_market_profit_and_loss(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listMarketProfitAndLoss')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.MarketProfitLoss, date_time_sent)

    def place_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'placeOrders')
        self.check_transaction_count(params)
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.PlaceOrders, date_time_sent)

    def cancel_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'cancelOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.CancelOrders, date_time_sent)

    def update_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'updateOrders')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.UpdateOrders, date_time_sent)

    def replace_orders(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'replaceOrders')
        self.check_transaction_count(params)
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.ReplaceOrders, date_time_sent)

    def set_next_hour(self):
        now = datetime.datetime.now()
        self._next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    def check_transaction_count(self, params):
        if datetime.datetime.now() > self._next_hour:
            self.set_next_hour()
            self.transaction_count = 0
        count = self.get_transaction_count(params)
        self.transaction_count += count
        if self.transaction_count > self.transaction_limit:
            raise TransactionCountError(self.transaction_count)

    @staticmethod
    def get_transaction_count(params):
        instructions = params.get('instructions')
        if instructions:
            return len(instructions)
        else:
            return 0
