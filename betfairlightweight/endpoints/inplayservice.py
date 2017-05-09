import datetime
from requests import ConnectionError

from ..exceptions import APIError
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint
from .. import resources


class InPlayService(BaseEndpoint):

    def get_event_timeline(self, event_id, session=None, lightweight=None):
        url = '%s%s' % (self.url, 'eventTimeline')
        params = {
            'eventId': event_id,
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        (response, elapsed_time) = self.request(params=params, session=session, url=url)
        return self.process_response(response, resources.EventTimeline, elapsed_time, lightweight)

    def get_scores(self, event_ids, session=None, lightweight=None):
        url = '%s%s' % (self.url, 'scores')
        params = {
            'eventIds': ','.join(str(x) for x in event_ids),
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        (response, elapsed_time) = self.request(params=params, session=session, url=url)
        return self.process_response(response, resources.Scores, elapsed_time, lightweight)

    def request(self, method=None, params=None, session=None, url=None):
        session = session or self.client.session
        date_time_sent = datetime.datetime.utcnow()
        try:
            response = session.get(url, params=params, headers=self.headers)
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)
        elapsed_time = (datetime.datetime.utcnow() - date_time_sent).total_seconds()

        response_data = response.json()

        check_status_code(response)
        return response_data, elapsed_time

    @property
    def headers(self):
        return {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        }

    @property
    def url(self):
        return 'https://www.betfair.com/inplayservice/v1.1/'
