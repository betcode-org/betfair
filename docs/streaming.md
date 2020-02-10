# Streaming

### Why streaming?

If your aim is to take a snapshot of horse markets 3 minutes before the off and at post time, polling (listMarketBook) is a good solution. You will only hit the Betfair API endpoint 2 times per market.
But if you want to gather, process and react to data more frequently (e.g. in-play horse racing), polling is inefficient and the reason lies in the way HTTP works. Every time you hit a Betfair API endpoint:

- Your machine establishes a new connection with the Betfair server.
- It sends an HTTP request and receives and HTTP response.
- HTTP requests/responses carry headers, so more data is sent/received.

Streaming is more efficient because:

- The connection gets established once.
- From that moment, data keeps flowing from Betfair to your machine.
- There are no data overheads as you would have with polling / HTTP.
- This results in faster data and less CPU from your machine (and Betfair's)

### Market

A market stream can be created like so:


```python
import queue
import threading

import betfairlightweight
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

trading = betfairlightweight.APIClient("username", "password", app_key="appKey")
trading.login()

# create queue
output_queue = queue.Queue()

# create stream listener
listener = betfairlightweight.StreamListener(output_queue=output_queue)

# create stream
stream = trading.streaming.create_stream(listener=listener)

# create filters (GB WIN racing)
market_filter = streaming_market_filter(
    event_type_ids=["7"], country_codes=["GB"], market_types=["WIN"]
)
market_data_filter = streaming_market_data_filter(
    fields=["EX_BEST_OFFERS", "EX_MARKET_DEF"], ladder_levels=3
)

# subscribe
streaming_unique_id = stream.subscribe_to_markets(
    market_filter=market_filter,
    market_data_filter=market_data_filter,
    conflate_ms=1000,  # send update every 1000ms
)

# start stream in a new thread (in production would need err handling)
t = threading.Thread(target=stream.start, daemon=True)
t.start()

# check for updates in output queue
while True:
    market_books = output_queue.get()
    print(market_books)

    for market_book in market_books:
        print(
            market_book,
            market_book.streaming_unique_id,  # unique id of stream (returned from subscribe request)
            market_book.streaming_update,  # json update received
            market_book.market_definition,  # streaming definition, similar to catalogue request
            market_book.publish_time,  # betfair publish time of update
        )
```

### Order

!!! warning
    The order stream does not include matched positions, these can be found by making a getCurrentOrders request. However 'price point' matched backs and matched lays are stored in the order cache in matched_lays / matched_backs.

Order stream is similar to market:

```python
import queue
import threading

import betfairlightweight
from betfairlightweight.filters import streaming_order_filter

trading = betfairlightweight.APIClient("username", "password", app_key="appKey")
trading.login()

# create queue
output_queue = queue.Queue()

# create stream listener
listener = betfairlightweight.StreamListener(output_queue=output_queue)

# create stream
stream = trading.streaming.create_stream(listener=listener)

# create filters (GB WIN racing)
order_filter = streaming_order_filter()

# subscribe
streaming_unique_id = stream.subscribe_to_orders(
    order_filter=order_filter,
    conflate_ms=1000,  # send update every 1000ms
)

# start stream in a new thread (in production would need err handling)
t = threading.Thread(target=stream.start, daemon=True)
t.start()

# check for updates in output queue
while True:
    current_orders = output_queue.get()
    print(current_orders)
```

### Historical

Betfairlightweight can also handle historical streaming data that has been purchased from [Betfair](https://historicdata.betfair.com/#/home) or collected yourself. 

```python
>>> trading = betfairlightweight.APIClient("username", "password")

    # create listener
>>> listener = HistoricalListener(max_latency=1e100)

    # create historical stream, update directory to file location
>>> stream = trading.streaming.create_historical_stream(
        directory="/tmp/BASIC-1.132153978",
        listener=listener,
    )

    # start stream
>>> stream.start()
```

The historical stream can be used in the same way as the market/order stream allowing backtesting / market processing.

### Snap

Instead of waiting for an update you can snap the listener to get an up to date version of the data.

```python
>>> market_books = listener.snap(
        market_ids=["1.12345323"]
    )
```

!!! tip
    The streaming unique id is returned in the marketBook / orderBook which allows multiple streams to be differentiated if multiple streams feed into the same queue.
    
    ```
    market_book.streaming_unique_id
    ```

### Resubscribe

If you have lost connection and need to resubscribe (prevents a full image being sent) you can provide the following:

```python
>>> streaming_unique_id = stream.subscribe_to_markets(
        market_filter=market_filter,
        market_data_filter=market_data_filter,
        conflate_ms=1000,  # send update every 1000ms
        initial_clk=listener.initial_clk,
        clk=listener.clk,
    )
```

### Error Handling

When used in production it is recommended not to start the stream in a new thread and forgot about it, it will break, errors need to be caught. 

Please see the example [examplestreamingerrhandling.py](https://github.com/liampauling/betfair/blob/master/examples/examplestreamingerrhandling.py)

### Listener

You can create a custom listener by overriding the listener class:

```python
import betfairlightweight


class MyListener(betfairlightweight.StreamListener):
    def on_data(self, raw_data: str) -> Optional[bool]:
        print(raw_data)


custom_listener = MyListener()
```
