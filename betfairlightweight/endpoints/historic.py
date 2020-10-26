import os
import time
import requests

from ..exceptions import APIError, InvalidResponse
from ..compat import json
from .baseendpoint import BaseEndpoint
from ..utils import clean_locals, check_status_code


class Historic(BaseEndpoint):
    def get_my_data(self, session: requests.Session = None) -> dict:
        """
        Returns a list of data descriptions for data which has been purchased by the signed in user.

        :param requests.session session: Requests session object

        :rtype: dict
        """
        params = clean_locals(locals())
        method = "GetMyData"
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return response_json

    def get_collection_options(
        self,
        sport: str,
        plan: str,
        from_day: str,
        from_month: str,
        from_year: str,
        to_day: str,
        to_month: str,
        to_year: str,
        event_id: str = None,
        event_name: str = None,
        market_types_collection: str = None,
        countries_collection: str = None,
        file_type_collection: str = None,
        session: requests.Session = None,
    ) -> dict:
        """
        Returns a dictionary of file counts by market_types, countries and file_types.

        :param sport: sport to filter data for.
        :param plan: plan type to filter for, Basic Plan, Advanced Plan or Pro Plan.
        :param from_day: day of month to start data from.
        :param from_month: month to start data from.
        :param from_year: year to start data from.
        :param to_day: day of month to end data at.
        :param to_month: month to end data at.
        :param to_year: year to end data at.
        :param event_id: id of a specific event to get data for.
        :param event_name: name of a specific event to get data for.
        :param market_types_collection: list of specific marketTypes to filter for.
        :param countries_collection: list of countries to filter for.
        :param file_type_collection: list of file types.
        :param requests.session session: Requests session object

        :rtype: dict
        """
        params = clean_locals(locals())
        method = "GetCollectionOptions"
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return response_json

    def get_data_size(
        self,
        sport: str,
        plan: str,
        from_day: str,
        from_month: str,
        from_year: str,
        to_day: str,
        to_month: str,
        to_year: str,
        event_id: str = None,
        event_name: str = None,
        market_types_collection: str = None,
        countries_collection: str = None,
        file_type_collection: str = None,
        session: requests.Session = None,
    ) -> dict:
        """
        Returns a dictionary of file count and combines size files.

        :param sport: sport to filter data for.
        :param plan: plan type to filter for, Basic Plan, Advanced Plan or Pro Plan.
        :param from_day: day of month to start data from.
        :param from_month: month to start data from.
        :param from_year: year to start data from.
        :param to_day: day of month to end data at.
        :param to_month: month to end data at.
        :param to_year: year to end data at.
        :param event_id: id of a specific event to get data for.
        :param event_name: name of a specific event to get data for.
        :param market_types_collection: list of specific marketTypes to filter for.
        :param countries_collection: list of countries to filter for.
        :param file_type_collection: list of file types.
        :param requests.session session: Requests session object

        :rtype: dict
        """
        params = clean_locals(locals())
        method = "GetAdvBasketDataSize"
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return response_json

    def get_file_list(
        self,
        sport: str,
        plan: str,
        from_day: str,
        from_month: str,
        from_year: str,
        to_day: str,
        to_month: str,
        to_year: str,
        event_id: str = None,
        event_name: str = None,
        market_types_collection: str = None,
        countries_collection: str = None,
        file_type_collection: str = None,
        session: requests.Session = None,
    ) -> dict:
        """
        Returns a list of files which can then be used to download.

        :param sport: sport to filter data for.
        :param plan: plan type to filter for, Basic Plan, Advanced Plan or Pro Plan.
        :param from_day: day of month to start data from.
        :param from_month: month to start data from.
        :param from_year: year to start data from.
        :param to_day: day of month to end data at.
        :param to_month: month to end data at.
        :param to_year: year to end data at.
        :param event_id: id of a specific event to get data for.
        :param event_name: name of a specific event to get data for.
        :param market_types_collection: list of specific marketTypes to filter for.
        :param countries_collection: list of countries to filter for.
        :param file_type_collection: list of file types.
        :param requests.session session: Requests session object

        :rtype: dict
        """
        params = clean_locals(locals())
        method = "DownloadListOfFiles"
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return response_json

    def download_file(
        self,
        file_path: str,
        store_directory: str = None,
        session: requests.Session = None,
    ) -> str:
        """
        Download a file from betfair historical and store in given directory or current directory.

        :param file_path: the file path as given by get_file_list method.
        :param store_directory: directory path to store data files in.
        :return: name of file.
        """
        local_filename = file_path.split("/")[-1]
        if store_directory:
            local_filename = os.path.join(store_directory, local_filename)
        session = session or self.client.session
        r = session.get(
            "%s%s" % (self.url, "DownloadFile"),
            params={"filePath": file_path},
            headers=self.headers,
            stream=True,
            timeout=(self.connect_timeout, self.read_timeout),
        )
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename

    def request(
        self, method: str = None, params: dict = None, session: requests.Session = None
    ) -> (dict, float):
        """
        :param str method: Betfair api-ng method to be used.
        :param dict params: Params to be used in request
        :param Session session: Requests session to be used, reduces latency.
        """
        session = session or self.client.session
        time_sent = time.time()
        try:
            response = session.post(
                "%s%s" % (self.url, method),
                data=json.dumps(params),
                headers=self.headers,
                timeout=(self.connect_timeout, self.read_timeout),
            )
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
        return {"ssoid": self.client.session_token, "Content-Type": "application/json"}

    @property
    def url(self) -> str:
        return "https://historicdata.betfair.com/api/"
