import requests
from typing import Union, List

from .baseendpoint import BaseEndpoint
from .. import resources
from ..utils import clean_locals


class Scores(BaseEndpoint):
    """
    Scores operations.
    """

    URI = "ScoresAPING/v1.0/"

    def list_race_details(
        self,
        meeting_ids: list = None,
        race_ids: list = None,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.RaceDetails]]:
        """
        Search for races to get their details.

        :param list meeting_ids: Optionally restricts the results to the specified meeting IDs.
        The unique Id for the meeting equivalent to the eventId for that specific race as
        returned by listEvents
        :param list race_ids: Optionally restricts the results to the specified race IDs. The
        unique Id for the race in the format meetingid.raceTime (hhmm). raceTime is in GMT
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.RaceDetails]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listRaceDetails")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.RaceDetails, elapsed_time, lightweight
        )

    # Following requires app key to be authorised

    def list_available_events(
        self,
        event_ids: list = None,
        event_type_ids: list = None,
        event_status: list = None,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.AvailableEvent]]:
        """
        Search for events that have live score data available.

        :param list event_ids: Optionally restricts the results to the specified event IDs
        :param list event_type_ids: Optionally restricts the results to the specified event type IDs
        :param list event_status: Optionally restricts the results to the specified event status
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.AvailableEvent]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listAvailableEvents")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.AvailableEvent, elapsed_time, lightweight
        )

    def list_scores(
        self,
        update_keys: list,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.Score]]:
        """
        Returns a list of current scores for the given events.

        :param list update_keys: The filter to select desired markets. All markets that match
        the criteria in the filter are selected e.g. [{'eventId': '28205674', 'lastUpdateSequenceProcessed': 2}]
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.Score]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listScores")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.Score, elapsed_time, lightweight
        )

    def list_incidents(
        self,
        update_keys: dict,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.Incidents]]:
        """
        Returns a list of incidents for the given events.

        :param dict update_keys: The filter to select desired markets. All markets that match
        the criteria in the filter are selected e.g. [{'eventId': '28205674', 'lastUpdateSequenceProcessed': 2}]
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.Incidents]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listIncidents")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.Incidents, elapsed_time, lightweight
        )

    @property
    def url(self) -> str:
        return "%s%s" % (self.client.api_uri, "scores/json-rpc/v1")
