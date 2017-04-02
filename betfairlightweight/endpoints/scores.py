import datetime

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals


class Scores(BaseEndpoint):
    """
    Scores operations.
    """

    URI = 'ScoresAPING/v1.0/'

    def list_race_details(self, meetingIds=None, raceIds=None, session=None):
        """
        Search for races to get their details.

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

    # Following requires app key to be authorised and has not been tested.

    def list_scores(self, updateKeys, session=None):
        """
        Returns a list of current scores for the given events.

        :param dict updateKeys: The filter to select desired markets. All markets that match
        the criteria in the filter are selected
        :param requests.session session: Requests session object

        :rtype: list[resources.Score]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listScores')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.Score, date_time_sent)

    def list_incidents(self, updateKeys, session=None):
        """
        Returns a list of incidents for the given events.

        :param dict updateKeys: The filter to select desired markets. All markets that match
        the criteria in the filter are selected
        :param requests.session session: Requests session object

        :rtype: list[resources.Incidents]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listIncidents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.Incidents, date_time_sent)

    def list_available_events(self, eventIds=None, eventTypeIds=None, eventStatus=None, session=None):
        """
        Search for events that have live score data available.

        :param list eventIds: Optionally restricts the results to the specified event IDs
        :param list eventTypeIds: Optionally restricts the results to the specified event type IDs
        :param list eventStatus: Optionally restricts the results to the specified event status
        :param requests.session session: Requests session object

        :rtype: list[resources.AvailableEvent]
        """
        params = clean_locals(locals())
        date_time_sent = datetime.datetime.utcnow()
        method = '%s%s' % (self.URI, 'listAvailableEvents')
        response = self.request(method, params, session)
        return self.process_response(response.json(), resources.AvailableEvent, date_time_sent)

    @property
    def url(self):
        return '%s%s' % (self.client.api_uri, 'scores/json-rpc/v1')
