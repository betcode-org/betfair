import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals


class Scores(BaseEndpoint):
    """
    Scores operations.
    """

    URI = 'ScoresAPING/v1.0/'

    def list_race_details(self, params=None, meetingIds=None, raceIds=None, session=None):
        """
        Search for races to get their details.

        :param dict params: json request, will be default if provided
        :param dict meetingIds: Optionally restricts the results to the specified meeting IDs.
        The unique Id for the meeting equivalent to the eventId for that specific race as
        returned by listEvents
        :param str raceIds: Optionally restricts the results to the specified race IDs. The
        unique Id for the race in the format meetingid.raceTime (hhmm). raceTime is in GMT
        :param requests.session session: Requests session object

        :rtype: list[resources.RaceDetail]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listRaceDetails')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.RaceDetails, date_time_sent)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'scores/json-rpc/v1')
