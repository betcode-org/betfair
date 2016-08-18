from ..exceptions import APIError
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint


class InPlayService(BaseEndpoint):

    def list_scores(self, params, session=None):
        return self.request(params=params, session=session)

    def request(self, method=None, params=None, session=None):
        session = session or self.client.session
        try:
            response = session.get(self.url, data=self.create_req(params=params),
                                   headers=self.client.request_headers)
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        return response

    @staticmethod
    def create_req(method=None, params=None):
        """
        :param method: Betfair api-ng method to be used.
        :param params: Params to be used in request.
        :return: Json payload.
        """
        data = {'eventIds': '[%s]' % ', '.join(map(str, params)),
                'alt': 'json',
                'productType': 'EXCHANGE',
                'regionCode': 'UK',
                'locale': 'en_GB'}
        return data

    @property
    def url(self):
        return 'https://www.betfair.com/inplayservice/v1.1'
