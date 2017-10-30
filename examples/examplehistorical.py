import logging

import betfairlightweight
from betfairlightweight import StreamListener
from betfairlightweight.streaming.stream import MarketStream

"""
Data needs to be downloaded from:
    https://historicdata.betfair.com
"""

# setup logging
logging.basicConfig(level=logging.INFO)

# create trading instance (no need to put in correct details)
trading = betfairlightweight.APIClient('username', 'password')

import queue
from pympler.tracker import SummaryTracker
tracker = SummaryTracker()

q = queue.Queue()

# create listener
listener = StreamListener(
    max_latency=1e100,
    output_queue=q
)

# create historical stream, update directory to file location
stream = trading.streaming.create_historical_stream(
    directory='examplessecret/horse-racing-pro-sample',
    listener=listener
)

# start stream
stream.start(async=True)

x = 0
while True:
    data = q.get()
    print(data[0].publish_time)
    x += 1
    if x % 100:
        tracker.print_diff()

tracker.print_diff()