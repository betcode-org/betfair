[![Build Status](https://travis-ci.org/LiamPa/betfairlightweight.svg?branch=master)](https://travis-ci.org/LiamPa/betfairlightweight)

# betfairlightweight

Lightweight, super fast python wrapper for Betfair API-NG allowing all betting operations (including market and order streaming) and some account operations.

# setup

Add your certificates to '/certs/' and app_key to environment variables with username as key before installing.

.bash_profile
```
# betfair
export username = "appkey"
```

The library can then be used as follows:

```python
import betfairlightweight

trading = betfairlightweight.APIClient('username', 'password', app_key='app_key')

trading.login()
```


```python
event_types = trading.list_event_types()
```

event_types is a list of classes containing data.

# streaming

Currently two listeners available, below will run the base listener which prints anything it receives.
Stream listener is able to hold multiple streams, hold a cache and push market_books/order_books out via a queue.


```python
betfair_socket = trading.create_stream(2, description='Test Market Socket')
betfair_socket.start(True)
betfair_socket.authenticate()
betfair_socket.subscribe_to_markets({'eventTypeIds': ['7'],
                                     'countryCodes': ['GB', 'IE'], 
                                     'marketTypes': ['WIN']},
                                    {'fields': ['EX_BEST_OFFERS', 'EX_MARKET_DEF'],
                                     'ladderLevels': 1})
```

# todo

    - Complete unit tests
    - Market and Order streaming added, need further tests
    - Fix issue with no errorCode in cancel request (details sent to bdp@betfair.com)
    - Use schematics for json -> data structure, schematics is slow as balls (0.3s+ for 300 marketBook request)
    - Enums for correct values to be sent
    - Choose where certs are located
    - Thread lock on transaction counter
