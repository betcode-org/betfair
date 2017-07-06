import logging

import betfairlightweight
from betfairlightweight import StreamListener
from betfairlightweight.streaming.stream import MarketStream

# setup logging
logging.basicConfig(level=logging.INFO)

# create trading instance (no need to put in correct details)
trading = betfairlightweight.APIClient('username', 'password')

# create custom listener and stream
class HistoricalStream(MarketStream):
    def __init__(self, unique_id, output_queue, max_latency, lightweight):
        super(HistoricalStream, self).__init__(unique_id, output_queue, max_latency, lightweight)
        with open('output.txt', 'w') as output:
            output.write('Time,MarketId,Status,Inplay,SelectionId,LastPriceTraded\n')

    def on_process(self, marketbooks):
        with open('output.txt', 'a') as output:
            for market_book in marketbooks:
                for runner in market_book.runners:
                    output.write('%s,%s,%s,%s,%s,%s\n' % (
                        market_book.publish_time, market_book.market_id, market_book.status, market_book.inplay,
                        runner.selection_id, runner.last_price_traded or ''
                    ))


class HistoricalListener(StreamListener):
    def _add_stream(self, unique_id, stream_type):
        if stream_type == 'marketSubscription':
            return HistoricalStream(
                unique_id, self.output_queue, self.max_latency, self.lightweight
            )

# create listener
listener = HistoricalListener(
    max_latency=1e100
)

# create historical stream
stream = trading.historical.create_stream(
    directory='/Users/liampauling/Downloads/Sites 3/xdw/api/c0a022d4-3460-41f1-af12-a0b68b136898/BASIC-1.132153978',
    listener=listener
)

# start stream
stream.start(async=False)
