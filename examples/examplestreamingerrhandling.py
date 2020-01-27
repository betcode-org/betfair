import logging
import queue
import threading
from tenacity import retry, wait_exponential

import betfairlightweight
from betfairlightweight import StreamListener
from betfairlightweight import BetfairError
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

"""
Streaming example to handle timeouts or connection errors, 
with reconnect.

Code uses 'tenacity' library for retrying.

Streaming class inherits threading module to simplify start/
stop.
"""

# setup logging
logging.basicConfig(level=logging.INFO)  # change to DEBUG to see log all updates
logger = logging.getLogger(__name__)


class Streaming(threading.Thread):
    def __init__(
        self,
        client: betfairlightweight.APIClient,
        market_filter: dict,
        market_data_filter: dict,
        conflate_ms: int = None,
        streaming_unique_id: int = 1000,
    ):
        threading.Thread.__init__(self, daemon=True, name=self.__class__.__name__)
        self.client = client
        self.market_filter = market_filter
        self.market_data_filter = market_data_filter
        self.conflate_ms = conflate_ms
        self.streaming_unique_id = streaming_unique_id
        self.stream = None
        self.output_queue = queue.Queue()
        self.listener = StreamListener(output_queue=self.output_queue)

    @retry(wait=wait_exponential(multiplier=1, min=2, max=20))
    def run(self) -> None:
        logger.info("Starting MarketStreaming")
        self.stream = self.client.streaming.create_stream(
            unique_id=self.streaming_unique_id, listener=self.listener
        )
        try:
            self.streaming_unique_id = self.stream.subscribe_to_markets(
                market_filter=self.market_filter,
                market_data_filter=self.market_data_filter,
                conflate_ms=self.conflate_ms,
                initial_clk=self.listener.initial_clk,  # supplying these two values allows a reconnect
                clk=self.listener.clk,
            )
            self.stream.start()
        except BetfairError:
            logger.error("MarketStreaming run error", exc_info=True)
            raise
        except Exception:
            logger.critical("MarketStreaming run error", exc_info=True)
            raise
        logger.info("Stopped MarketStreaming {0}".format(self.streaming_unique_id))

    def stop(self) -> None:
        if self.stream:
            self.stream.stop()


# create trading instance (app key must be activated for streaming)
trading = betfairlightweight.APIClient("username", "password", app_key="appKey")

# login
trading.login_interactive()

# create filters (GB WIN racing)
market_filter = streaming_market_filter(
    event_type_ids=["7"], country_codes=["GB"], market_types=["WIN"]
)
market_data_filter = streaming_market_data_filter(
    fields=["EX_BEST_OFFERS", "EX_MARKET_DEF"], ladder_levels=3
)

# create streaming object
streaming = Streaming(trading, market_filter, market_data_filter)

# start streaming (runs in new thread and handles any errors)
streaming.start()

# check for updates in output queue
while True:
    market_books = streaming.output_queue.get()
    print(market_books)

    for market_book in market_books:
        print(
            market_book,
            market_book.streaming_unique_id,  # unique id of stream (returned from subscribe request)
            market_book.streaming_update,  # json update received
            market_book.market_definition,  # streaming definition, similar to catalogue request
            market_book.publish_time,  # betfair publish time of update
        )
