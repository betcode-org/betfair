import time
import requests
from typing import Union, List

from ..exceptions import APIError, InvalidResponse
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint
from .. import resources
from ..compat import json


class InPlayService(BaseEndpoint):
    """
    In play service operations.
    """

    def get_event_timeline(
        self, event_id: int, session: requests.Session = None, lightweight: bool = None
    ) -> Union[list, resources.EventTimeline]:
        """
        Returns event timeline for event id provided.

        :param int event_id: Event id to return
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.EventTimeline
        """
        url = "%s%s" % (self.url, "eventTimeline")
        params = {
            "eventId": event_id,
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        (response, response_json, elapsed_time) = self.request(
            params=params, session=session, url=url
        )
        return self.process_response(
            response_json, resources.EventTimeline, elapsed_time, lightweight
        )

    def get_event_timelines(
        self,
        event_ids: list,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.EventTimeline]]:
        """
        Returns a list of event timelines based on event id's
        supplied.

        :param list event_ids: List of event id's to return
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.EventTimeline]
        """
        url = "%s%s" % (self.url, "eventTimelines")
        params = {
            "eventIds": ",".join(str(x) for x in event_ids),
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        (response, response_json, elapsed_time) = self.request(
            params=params, session=session, url=url
        )
        return self.process_response(
            response_json, resources.EventTimeline, elapsed_time, lightweight
        )

    def get_scores(
        self,
        event_ids: list,
        session: requests.Session = None,
        lightweight: bool = None,
    ) -> Union[list, List[resources.Scores]]:
        """
        Returns a list of scores based on event id's
        supplied.

        :param list event_ids: List of event id's to return
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.Scores]
        """
        url = "%s%s" % (self.url, "scores")
        params = {
            "eventIds": ",".join(str(x) for x in event_ids),
            "alt": "json",
            "regionCode": "UK",
            "locale": "en_GB",
        }
        (response, response_json, elapsed_time) = self.request(
            params=params, session=session, url=url
        )
        return self.process_response(
            response_json, resources.Scores, elapsed_time, lightweight
        )

    def request(
        self,
        method: str = None,
        params: dict = None,
        session: requests.Session = None,
        url: str = None,
    ) -> (dict, float):
        session = session or self.client.session
        time_sent = time.time()
        try:
            response = session.get(url, params=params, headers=self.headers)
        except requests.ConnectionError as e:
            raise APIError(None, method, params, e)
        except Exception as e:
            raise APIError(None, method, params, e)
        elapsed_time = time.time() - time_sent

        check_status_code(response)
        try:
            response_json = json.loads(response.content.decode("utf-8"))
        except ValueError:
            raise InvalidResponse(response.text)

        return response, response_json, elapsed_time

    @property
    def headers(self) -> dict:
        return {"Connection": "keep-alive", "Content-Type": "application/json"}

    @property
    def url(self) -> str:
        return "https://ips.betfair.com/inplayservice/v1.1/"
