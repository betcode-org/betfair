import os
import logging
import queue

import betfairlightweight
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)


# setup logging
logging.basicConfig(level=logging.INFO)  # change to DEBUG to see log all updates

# create trading instance (app key must be activated for streaming)
username = os.environ.get('username')
trading = betfairlightweight.APIClient(username)
trading.login()

# create queue
output_queue = queue.Queue()

# create stream listener
listener = betfairlightweight.StreamListener(
    output_queue=output_queue,
)

# create stream
stream = trading.streaming.create_stream(
    listener=listener,
)

# create filters (GB WIN racing)
market_filter = streaming_market_filter(
    event_type_ids=['7'],
    country_codes=['GB'],
    market_types=['WIN'],
)
market_data_filter = streaming_market_data_filter(
    fields=['EX_BEST_OFFERS', 'EX_MARKET_DEF'],
    ladder_levels=3,
)

# subscribe
streaming_unique_id = stream.subscribe_to_markets(
    market_filter=market_filter,
    market_data_filter=market_data_filter,
    conflate_ms=1000,  # send update every 1000ms
)

# start stream
stream.start(async=True)

"""
Data can also be accessed by using the snap function in the listener, e.g:

    market_books = listener.snap(
        market_ids=[1.12345323]
    )

Errors need to be caught at stream.start, resubscribe can then be used to
prevent full image being sent, e.g:

    streaming_unique_id = stream.subscribe_to_markets(
        market_filter=market_filter,
        market_data_filter=market_data_filter,
        conflate_ms=1000,  # send update every 1000ms
        initial_clk=listener.initial_clk,
        clk=listener.clk,
    )

The streaming unique id is returned in the market book which allows multiple
streams to be differentiated if multiple streams feed into the same queue.
"""

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
            market_book.publish_time  # betfair publish time of update
        )
