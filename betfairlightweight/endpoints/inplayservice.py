import datetime
from requests import ConnectionError

from ..exceptions import APIError
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint
from .. import resources


class InPlayService(BaseEndpoint):

    def get_event_timeline(self, event_id, session=None):
        date_time_sent = datetime.datetime.utcnow()
        url = '%s%s' % (self.url, 'eventTimeline')
        params = {
            'eventId': event_id,
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        response = self.request(params=params, session=session, url=url)
        return self.process_response(response.json(), resources.EventTimeline, date_time_sent)

    def get_scores(self, event_ids, session=None):
        date_time_sent = datetime.datetime.utcnow()
        url = '%s%s' % (self.url, 'scores')
        params = {
            'eventIds': ','.join(str(x) for x in event_ids),
            'alt': 'json',
            'regionCode': 'UK',
            'locale': 'en_GB'
        }
        response = self.request(params=params, session=session, url=url)
        return self.process_response(response.json(), resources.Scores, date_time_sent)

    def request(self, method=None, params=None, session=None, url=None):
        session = session or self.client.session
        try:
            response = session.get(url, params=params, headers=self.headers)
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        return response

    @property
    def headers(self):
        return {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        }

    @property
    def url(self):
        return 'https://www.betfair.com/inplayservice/v1.1/'
