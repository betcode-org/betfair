import requests
from typing import Union, List

from ..exceptions import RaceCardError, InvalidResponse
from ..utils import request
from .baseendpoint import BaseEndpoint
from .. import resources


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
        try:
            response, data, duration = request(
                session=session or self.client.session,
                method="get",
                url=self.url,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
            )
            if "appKey" in data:
                return data["appKey"]
        except InvalidResponse:
            pass
        # the response was not JSON or did not contain an app key
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
        return request(
            session=session or self.client.session,
            method="get",
            url=self.url + self.method,
            params=params,
            headers=self.headers,
            connect_timeout=self.connect_timeout,
            read_timeout=self.read_timeout,
        )

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
