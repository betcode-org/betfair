# betfairlightweight

[![Build Status](https://travis-ci.org/liampauling/betfairlightweight.svg?branch=master)](https://travis-ci.org/liampauling/betfairlightweight) [![Coverage Status](https://coveralls.io/repos/github/liampauling/betfairlightweight/badge.svg?branch=master)](https://coveralls.io/github/liampauling/betfairlightweight?branch=master) [![PyPI version](https://badge.fury.io/py/betfairlightweight.svg)](https://pypi.python.org/pypi/betfairlightweight)

Lightweight, super fast pythonic wrapper for [Betfair API-NG](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and most account operations.

[Documentation](https://github.com/liampauling/betfairlightweight/wiki)

Currently tested on Python 2.7, 3.4, 3.5 and 3.6.

# installation

```
$ pip install betfairlightweight
```

# setup

Add your certificates to '/certs/' and app_key to environment variables with username as key before using.

.bash_profile
```
export username = "appkey"
```

The library can then be used as follows:

```python
>>> import betfairlightweight

>>> trading = betfairlightweight.APIClient('username', 'password', app_key='app_key')

>>> trading.login()
```


```python
>>> event_types = trading.betting.list_event_types()

[<EventTypeResult>, <EventTypeResult>, ..]
```


# streaming

Currently two listeners available, below will run the base listener which prints anything it receives.
Stream listener is able to hold an order stream and a market stream, although it is recommended to have one socket per
stream. The listener can hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

```python
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

betfair_socket = trading.streaming.create_stream(unique_id=2, description='Test Market Socket')

market_filter = streaming_market_filter(
    eventTypeIds=['7'],
    countryCodes=['IE'],
    marketTypes=['WIN'],
)
market_data_filter = streaming_market_data_filter(
    fields=['EX_ALL_OFFERS', 'EX_MARKET_DEF'],
    ladderLevels=3
)

betfair_socket.subscribe_to_markets(
    unique_id=12345,
    market_filter=market_filter,
    market_data_filter=market_data_filter
)
betfair_socket.start(async=False)
```
