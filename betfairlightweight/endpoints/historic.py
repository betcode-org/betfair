import os
import requests
import datetime
from requests import ConnectionError

from ..exceptions import (
    APIError,
    InvalidResponse,
)
from ..compat import json
# from .. import resources
from .baseendpoint import BaseEndpoint
from ..utils import clean_locals, check_status_code

# monkeypatching requests
# https://github.com/kennethreitz/requests/issues/1595
requests.models.json = json


class Historic(BaseEndpoint):

    def get_my_data(self, session=None):
        """
        Returns a list of data descriptions for data which has been purchased by the signed in user.

        :param requests.session session: Requests session object

        :rtype: dict
        """
        params = clean_locals(locals())
        method = 'GetMyData'
        (response, elapsed_time) = self.request(method, params, session)
        return response

    def get_collection_options(self, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year,
                                  event_id=None, event_name=None, market_types_collection=None,
                                  countries_collection=None, file_type_collection=None, session=None):
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
        method = 'GetCollectionOptions'
        (response, elapsed_time) = self.request(method, params, session)
        return response

    def get_data_size(self, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year, event_id=None,
                      event_name=None, market_types_collection=None, countries_collection=None,
                      file_type_collection=None, session=None):
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
        method = 'GetAdvBasketDataSize'
        (response, elapsed_time) = self.request(method, params, session)
        return response

    def get_file_list(self, sport, plan, from_day, from_month, from_year, to_day, to_month, to_year, event_id=None,
                      event_name=None, market_types_collection=None, countries_collection=None,
                      file_type_collection=None, session=None):
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
        method = 'DownloadListOfFiles'
        (response, elapsed_time) = self.request(method, params, session)
        return response

    def download_file(self, file_path, store_directory=None, chunk_size=1024):
        """
        Download a file from betfair historical and store in given directory or current directory.

        :param file_path: the file path as given by get_file_list method.
        :param store_directory: directory path to store data files in.
        :param chunk_size: download chunk size; if None, do not stream download
        :return: name of file.
        """
        local_filename = file_path.split('/')[-1]
        if store_directory:
            local_filename = os.path.join(store_directory, local_filename)

        r = requests.get(
            '%s%s' % (self.url, 'DownloadFile'),
            params={'filePath': file_path},
            headers=self.headers,
            stream=True if chunk_size is not None else False,
        )
        with open(local_filename, 'wb') as f:
            if chunk_size is not None:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            else:
                f.write(r.content)

        return local_filename

    def request(self, method, params, session):
        """
        :param str method: Betfair api-ng method to be used.
        :param dict params: Params to be used in request
        :param Session session: Requests session to be used, reduces latency.
        """
        session = session or self.client.session
        date_time_sent = datetime.datetime.utcnow()
        try:
            response = session.post(
                '%s%s' % (self.url, method),
                data=json.dumps(params),
                headers=self.headers,
                timeout=(self.connect_timeout, self.read_timeout)
            )
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)
        elapsed_time = (datetime.datetime.utcnow()-date_time_sent).total_seconds()

        check_status_code(response)
        try:
            response_data = response.json()
        except ValueError:
            raise InvalidResponse(response.text)

        return response_data, elapsed_time

    @property
    def headers(self):
        return {
            'ssoid': self.client.session_token,
            'Content-Type': 'application/json',
        }

    @property
    def url(self):
        return 'https://historicdata.betfair.com/api/'
