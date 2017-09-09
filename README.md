# betfairlightweight

[![Build Status](https://travis-ci.org/liampauling/betfair.svg?branch=master)](https://travis-ci.org/liampauling/betfair) [![Coverage Status](https://coveralls.io/repos/github/liampauling/betfair/badge.svg?branch=master)](https://coveralls.io/github/liampauling/betfair?branch=master) [![PyPI version](https://badge.fury.io/py/betfairlightweight.svg)](https://pypi.python.org/pypi/betfairlightweight)

Lightweight, super fast (uses c libraries) pythonic wrapper for [Betfair API-NG](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and most account operations, see [examples](https://github.com/liampauling/betfair/tree/master/examples).

[Documentation](https://github.com/liampauling/betfair/wiki)

[Join slack group](https://betfairlightweight.herokuapp.com)

Currently tested on Python 2.7, 3.4, 3.5 and 3.6.

# installation

```
$ pip install betfairlightweight
```

# setup

Add your certificates to '/certs/' and app_key (optional) to environment variables with username as key before using.

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

Currently two listeners available, below will run the base listener which prints anything it receives. Stream listener is able to hold an order stream or a market stream (one per listener). The listener can hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

In development so breaking changes likely.

```python
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

betfair_socket = trading.streaming.create_stream(
    unique_id=0,
    description='Test Market Socket',
)

market_filter = streaming_market_filter(
    event_type_ids=['7'],
    country_codes=['IE'],
    market_types=['WIN'],
)
market_data_filter = streaming_market_data_filter(
    fields=['EX_ALL_OFFERS', 'EX_MARKET_DEF'],
    ladder_levels=3
)

betfair_socket.subscribe_to_markets(
    market_filter=market_filter,
    market_data_filter=market_data_filter,
)
betfair_socket.start(async=False)
```

# historical data

Taking advantage of the streaming code lightweight can parse/output historical data in the same way it process streaming data allowing backtesting or with a custom listener, csv creation (see [examples](https://github.com/liampauling/betfair/tree/master/examples)).

[Historical Data](https://historicdata.betfair.com/#/home)

In development so breaking changes likely.

```python

stream = trading.streaming.create_historical_stream(
    directory='horse-racing-pro-sample',
)

stream.start(async=False)
```
