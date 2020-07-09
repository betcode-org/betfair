import re
import time
import requests
from typing import Union, List

from ..exceptions import APIError, RaceCardError, InvalidResponse
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint
from .. import resources
from ..compat import json


class RaceCard(BaseEndpoint):
    """
    RaceCard operations.
    """

    app_key = None

    def login(self, session: requests.Session = None) -> None:
        """
        Parses app key from betfair exchange site.

        :param requests.session session: Requests session object
        """
        session = session or self.client.session
        try:
            response = session.get(self.login_url)
        except requests.ConnectionError as e:
            raise APIError(None, self.login_url, None, e)
        except Exception as e:
            raise APIError(None, self.login_url, None, e)
        app_key = re.findall(
            r'''"appKey":\s"(.*?)"''', response.content.decode("utf-8")
        )
        if app_key:
            self.app_key = app_key[0]
        else:
            raise RaceCardError("Unable to find appKey")

    def get_race_card(
        self,
        market_ids: list,
        data_entries: str = None,
        session: requests.Session = None,
        lightweight: bool = False,
    ) -> Union[list, List[resources.RaceCard]]:
        """
        Returns a list of race cards based on market ids provided.

        :param list market_ids: The filter to select desired markets
        :param str data_entries: Data to be returned
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.RaceCard]
        """
        if not self.app_key:
            raise RaceCardError(
                "You need to login before requesting a race_card\n"
                "APIClient.race_card.login()"
            )
        params = self.create_race_card_req(market_ids, data_entries)
        (response, response_json, elapsed_time) = self.request(
            "raceCard", params=params, session=session
        )
        return self.process_response(
            response_json, resources.RaceCard, elapsed_time, lightweight
        )

    def get_race_result(
        self,
        market_ids: list,
        data_entries: str = None,
        session: requests.Session = None,
        lightweight: bool = True,
    ) -> list:
        """
        Returns a list of race results based on event ids provided.

        :param list market_ids: The filter to select desired events
        :param str data_entries: Data to be returned
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.RaceResult]
        """
        if not self.app_key:
            raise RaceCardError(
                "You need to login before requesting a race_card\n"
                "APIClient.race_card.login()"
            )
        params = self.create_race_result_req(market_ids, data_entries)
        (response, response_json, elapsed_time) = self.request(
            "raceResults", params=params, session=session
        )
        return self.process_response(response_json, None, elapsed_time, lightweight)

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> (dict, float):
        session = session or self.client.session
        time_sent = time.time()
        url = "%s%s" % (self.url, method)
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

    @staticmethod
    def create_race_card_req(market_ids: list, data_entries: str) -> dict:
        if not data_entries:
            data_entries = "RACE, TIMEFORM_DATA, RUNNERS, RUNNER_DETAILS"
        return {"dataEntries": data_entries, "marketId": ",".join(market_ids)}

    @staticmethod
    def create_race_result_req(market_ids: list, data_entries: str) -> dict:
        if not data_entries:
            data_entries = "RUNNERS, MARKETS, PRICES, RACE, COURSE"
        return {
            "dataEntries": data_entries,
            "marketId": ",".join(market_ids),
            "sortBy": "DATE_DESC",
        }

    @property
    def headers(self) -> dict:
        return {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-Application": self.app_key,
        }

    @property
    def login_url(self) -> str:
        return "https://www.betfair.com/exchange/plus/"

    @property
    def url(self) -> str:
        return "https://www.betfair.com/rest/v2/"
