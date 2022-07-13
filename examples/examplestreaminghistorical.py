import logging

import betfairlightweight
from betfairlightweight import StreamListener

"""
Data needs to be downloaded from:
    https://historicdata.betfair.com
    
smart-open library recommended for opening bz2/gz files
"""

# setup logging
logging.basicConfig(level=logging.INFO)

# create trading instance (don't need username/password)
trading = betfairlightweight.APIClient("username", "password")

# create listener
listener = StreamListener(max_latency=None)

# create historical stream (update file_path to your file location)
stream = trading.streaming.create_historical_generator_stream(
    file_path="/tmp/BASIC-1.132153978",
    listener=listener,
)

# create generator
gen = stream.get_generator()

# print marketBooks
for market_books in gen():
    for market_book in market_books:
        print(market_book)

# print based on seconds to start
for market_books in gen():
    for market_book in market_books:
        seconds_to_start = (
            market_book.market_definition.market_time - market_book.publish_time
        ).total_seconds()
        if seconds_to_start < 100:
            print(market_book.market_id, seconds_to_start, market_book.total_matched)

        # print winner details once market is closed
        if market_book.status == "CLOSED":
            for runner in market_book.runners:
                if runner.status == "WINNER":
                    print(
                        "{0}: {1} with sp of {2}".format(
                            runner.status, runner.selection_id, runner.sp.actual_sp
                        )
                    )

# record prices to a file
with open("output.txt", "w") as output:
    output.write("Time,MarketId,Status,Inplay,SelectionId,LastPriceTraded\n")

for market_books in gen():
    for market_book in market_books:
        with open("output.txt", "a") as output:
            for runner in market_book.runners:
                # how to get runner details from the market definition
                market_def = market_book.market_definition
                runners_dict = {
                    (runner.selection_id, runner.handicap): runner
                    for runner in market_def.runners
                }
                runner_def = runners_dict.get((runner.selection_id, runner.handicap))

                output.write(
                    "%s,%s,%s,%s,%s,%s\n"
                    % (
                        market_book.publish_time,
                        market_book.market_id,
                        market_book.status,
                        market_book.inplay,
                        runner.selection_id,
                        runner.last_price_traded or "",
                    )
                )
