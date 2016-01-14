
filter = {'textQuery': 'barclays',
          'exchangeIds': ['7'],
          'eventTypeIds': ['7'],
          'eventIds': ['7'],
          'competitionIds': ['34'],
          'marketIds': ['1.122575546'],
          'venues': ['GB'],
          'bspOnly': True,
          'turnInPlayEnabled': True,
          'inPlayOnly': True,
          'marketBettingTypes': ['ODDS', 'ASIAN_HANDICAP_SINGLE_LINE', 'ASIAN_HANDICAP_DOUBLE_LINE'],
          'marketCountries': ['GB'],
          'marketTypeCodes': ['WIN'],
          'marketStartTime': {'from': '2016-01-14T01:15:00Z',
                              'to': '2016-01-21T02:30:00Z'},
          'withOrders': ['EXECUTION_COMPLETE', 'EXECUTABLE'],
          'locale': 'en'}


params = {'filter': {}}

listTimeRanges = {'filter': {},
                  'granularity': 'DAYS'}

listMarketCatalogue = {'filter': {},
                       'sort': 'MINIMUM_TRADED',
                       'maxResults': '1',
                       'marketProjection': ['COMPETITION', 'EVENT', 'EVENT_TYPE', 'MARKET_DESCRIPTION',
                                            'RUNNER_DESCRIPTION', 'RUNNER_METADATA', 'MARKET_START_TIME']}

listMarketBook = {'priceProjection': {'priceData': ['SP_AVAILABLE', 'SP_TRADED', 'EX_BEST_OFFERS',
                                                    'EX_ALL_OFFERS', 'EX_TRADED'],
                                      'virtualise': True,
                                      'exBestOffersOverrides': {'bestPricesDepth': '2',
                                                                'rollupModel': 'PAYOUT',
                                                                'rollupLimit': '2'}
                                      },
                  'orderProjection': 'ALL',  # 'EXECUTABLE', 'EXECUTION_COMPLETE'
                  'matchProjection': 'NO_ROLLUP',  # 'ROLLED_UP_BY_PRICE', 'ROLLED_UP_BY_AVG_PRICE'
                  'currencyCode': 'USD'}
