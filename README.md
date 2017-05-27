# betfairlightweight

[![Build Status](https://travis-ci.org/liampauling/betfairlightweight.svg?branch=master)](https://travis-ci.org/liampauling/betfairlightweight) [![Coverage Status](https://coveralls.io/repos/github/liampauling/betfairlightweight/badge.svg?branch=master)](https://coveralls.io/github/liampauling/betfairlightweight?branch=master) [![PyPI version](https://badge.fury.io/py/betfairlightweight.svg)](https://pypi.python.org/pypi/betfairlightweight) [![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors)

Lightweight, super fast (uses c libraries) pythonic wrapper for [Betfair API-NG](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and most account operations, see examples.

[Documentation](https://github.com/liampauling/betfairlightweight/wiki)

[Join slack group](https://betfairlightweight.herokuapp.com)

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

Currently two listeners available, below will run the base listener which prints anything it receives. Stream listener is able to hold an order stream or a market stream (one per listener). The listener can hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

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

## Contributors

Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!