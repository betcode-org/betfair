import datetime

from .baseendpoint import BaseEndpoint
from .. import resources


class Scores(BaseEndpoint):

    URI = 'ScoresAPING/v1.0/'

    def list_race_details(self, params=None, session=None):
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listRaceDetails')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.RaceDetails, date_time_sent)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'scores/json-rpc/v1')
