import datetime

from .baseendpoint import BaseEndpoint
from ..resources.resources import EventTypes


class Betting(BaseEndpoint):

    URI = 'SportsAPING/v1.0/'

    def list_event_types(self, params=None):
        date_time_sent = datetime.datetime.now()
        method = '%s%s' % (self.URI, 'listEventTypes')
        response = self.request(method, params)
        return self.process_response(response.json(), EventTypes, date_time_sent)
