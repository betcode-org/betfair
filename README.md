# betfairlightweight

[![Build Status](https://travis-ci.org/liampauling/betfair.svg?branch=master)](https://travis-ci.org/liampauling/betfair) [![Coverage Status](https://coveralls.io/repos/github/liampauling/betfair/badge.svg?branch=master)](https://coveralls.io/github/liampauling/betfair?branch=master) [![PyPI version](https://badge.fury.io/py/betfairlightweight.svg)](https://pypi.python.org/pypi/betfairlightweight)

Lightweight, super fast (uses c libraries) pythonic wrapper for [Betfair API-NG](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and most account operations, see [examples](https://github.com/liampauling/betfair/tree/master/examples).

[Documentation](https://github.com/liampauling/betfair/wiki)

[Join slack group](https://betfairlightweight.herokuapp.com)

Currently tested on Python 2.7, 3.4, 3.5, 3.6 and 3.7.

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

Following endpoints are available:

- trading.[login](http://docs.developer.betfair.com/docs/pages/viewpage.action?pageId=3834909#Login&SessionManagement-Login)
- trading.[keep_alive](http://docs.developer.betfair.com/docs/pages/viewpage.action?pageId=3834909#Login&SessionManagement-KeepAlive)
- trading.[logout](http://docs.developer.betfair.com/docs/pages/viewpage.action?pageId=3834909#Login&SessionManagement-Logout)

- trading.[betting](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Betting+API)
- trading.[account](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Accounts+API)
- trading.[navigation](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Navigation+Data+For+Applications)
- trading.[scores](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Race+Status+API)
- trading.[streaming](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)
- trading.[historical](https://historicdata.betfair.com/#/apidocs)

- trading.in_play_service
- trading.race_card


# streaming

Currently two listeners available, below will run the base listener which prints anything it receives. Stream listener is able to hold an order stream or a market stream (one per listener). The listener can hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

In development so breaking changes likely.

```python
>>> from betfairlightweight.filters import (
        streaming_market_filter,
        streaming_market_data_filter,
    )

>>> betfair_socket = trading.streaming.create_stream(
        unique_id=0,
        description='Test Market Socket',
    )

>>> market_filter = streaming_market_filter(
        event_type_ids=['7'],
        country_codes=['IE'],
        market_types=['WIN'],
    )
>>> market_data_filter = streaming_market_data_filter(
        fields=['EX_ALL_OFFERS', 'EX_MARKET_DEF'],
        ladder_levels=3
    )

>>> betfair_socket.subscribe_to_markets(
        market_filter=market_filter,
        market_data_filter=market_data_filter,
    )

>>> betfair_socket.start(_async=False)
```

# historic data

The historic endpoint provides some basic abstraction for the historicdata api:

[Historic Data API](https://historicdata.betfair.com/#/apidocs)

```python

>>> trading.historic.get_my_data()

[{'plan': 'Basic Plan', 'purchaseItemId': 1343, 'sport': 'Cricket', 'forDate': '2017-06-01T00:00:00'}]
```

Taking advantage of the streaming code lightweight can parse/output historical data in the same way it process streaming data allowing backtesting or with a custom listener, csv creation (see [examples](https://github.com/liampauling/betfair/tree/master/examples)).

[Historic Data](https://historicdata.betfair.com/#/home)

In development so breaking changes likely.

```python

>>> stream = trading.streaming.create_historical_stream(
        directory='horse-racing-pro-sample',
    )

>>> stream.start(_async=False)
```
