
# betfairlightweight

![Build Status](https://github.com/liampauling/betfair/workflows/test/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/liampauling/betfair/badge.svg?branch=master)](https://coveralls.io/github/liampauling/betfair?branch=master) [![PyPI version](https://badge.fury.io/py/betfairlightweight.svg)](https://pypi.python.org/pypi/betfairlightweight) [![Downloads](https://pepy.tech/badge/betfairlightweight)](https://pepy.tech/project/betfairlightweight)

Lightweight, super fast (uses C and Rust libraries) pythonic wrapper for [Betfair API-NG](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and account operations, see [examples](https://github.com/liampauling/betfair/tree/master/examples).

[docs](https://liampauling.github.io/betfair/)

[join slack group](https://betfairlightweight.herokuapp.com)

Currently tested on Python 3.6, 3.7, 3.8 and 3.9.

# installation

```bash
$ pip install betfairlightweight
```

To use C/Rust libraries install with

```bash
$ pip install betfairlightweight[speed]
```

# setup

In order to connect to the Betfair API you will need an App Key, SSL Certificates and a username/password.

### App Key
Follow [these](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Application+Keys) instructions to get your app key, you can either use a delayed or live key.

### SSL certificates
Follow [these](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login) instructions to set up your SSL certificates. Save your .ctr and .key files to a local directory. The default directory where the library is looking for the keys is '/certs' but you can specify any other directory.

### Using the library

The library can then be used as follows:

```python
import betfairlightweight

trading = betfairlightweight.APIClient('username', 'password', app_key='app_key', certs='/certs')

trading.login()
```

or the following for interactive login with no certs (not as secure)

```python
import betfairlightweight

trading = betfairlightweight.APIClient('username', 'password', app_key='app_key')

trading.login_interactive()
```


```python
event_types = trading.betting.list_event_types()

[<EventTypeResult>, <EventTypeResult>, ..]
```

Following endpoints are available:

- trading.[login](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login)
- trading.[login_interactive](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Interactive+Login+-+API+Endpoint)
- trading.[keep_alive](https://docs.developer.betfair.com/pages/viewpage.action?pageId=3834909#Login&SessionManagement-KeepAlive)
- trading.[logout](https://docs.developer.betfair.com/pages/viewpage.action?pageId=3834909#Login&SessionManagement-Logout)

- trading.[betting](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Betting+API)
- trading.[account](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Accounts+API)
- trading.[navigation](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Navigation+Data+For+Applications)
- trading.[scores](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Race+Status+API)
- trading.[streaming](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)
- trading.[historical](https://historicdata.betfair.com/#/apidocs)

- trading.in_play_service
- trading.race_card


# streaming

Currently two listeners available, below will run the base listener which prints anything it receives. Stream listener is able to hold an order stream or a market stream (one per listener). The listener can hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

```python
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

betfair_socket = trading.streaming.create_stream()

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

betfair_socket.start()  # blocking
```

# historic data

The historic endpoint provides some basic abstraction for the historicdata api:

[Historic Data API](https://historicdata.betfair.com/#/apidocs)

```python

trading.historic.get_my_data()

[{'plan': 'Basic Plan', 'purchaseItemId': 1343, 'sport': 'Cricket', 'forDate': '2017-06-01T00:00:00'}]
```

Taking advantage of the streaming code lightweight can parse/output historical data in the same way it process streaming data allowing backtesting or with a custom listener, csv creation (see [examples](https://github.com/liampauling/betfair/tree/master/examples)).

[Historic Data](https://historicdata.betfair.com/#/home)

```python

stream = trading.streaming.create_historical_stream(
    file_path='horse-racing-pro-sample',
)

stream.start()
```

or use the  stream generator:

```python

stream = trading.streaming.create_historical_generator_stream(
    file_path='horse-racing-pro-sample',
)

g = stream.get_generator()

for market_books in g():
    print(market_books)
```
