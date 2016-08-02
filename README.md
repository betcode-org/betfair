[![Build Status](https://travis-ci.org/LiamPa/betfairlightweight.svg?branch=version_0_3_0)](https://travis-ci.org/LiamPa/betfairlightweight)

# betfairlightweight

Lightweight, super fast python wrapper for [Betfair API-NG](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and most account operations.

python3 only.

[Documentation](https://github.com/LiamPa/betfairlightweight/wiki)

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
event_types = trading.betting.list_event_types()
```


# streaming

Currently two listeners available, below will run the base listener which prints anything it receives.
Stream listener is able to hold multiple streams, hold a cache and push market_books/order_books out via a queue.

[Exchange Stream API](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)

```python
betfair_socket = trading.streaming.create_stream(2, description='Test Market Socket')
betfair_socket.start(True)
betfair_socket.authenticate()
betfair_socket.subscribe_to_markets({'eventTypeIds': ['7'],
                                     'countryCodes': ['GB', 'IE'], 
                                     'marketTypes': ['WIN']},
                                    {'fields': ['EX_BEST_OFFERS', 'EX_MARKET_DEF'],
                                     'ladderLevels': 1})
```
