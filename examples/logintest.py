import apirequest
import apiclient
import logging


logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.ERROR,)


trading = apiclient.APIClient('username', 'password')

apirequest.login(trading)

# apirequest.keep_alive(trading)


params = {"marketIds": ["1.122481996"],
          'priceProjection': {'priceData': ['EX_TRADED']},
          'orderProjection': 'ALL',
          'matchProjection': 'ROLLED_UP_BY_PRICE',}

params = {'filter': {},
                       'sort': 'MINIMUM_TRADED',
                       'maxResults': '1000',
                       'marketProjection': ['COMPETITION', 'EVENT', 'EVENT_TYPE', 'MARKET_DESCRIPTION',
                                            'RUNNER_DESCRIPTION', 'RUNNER_METADATA', 'MARKET_START_TIME']}

# params = {'dateRange': {}}

# params = {'mar': [1]}

data = apirequest.list_market_catalogue(trading, params)
print(data)


apirequest.logout(trading)
