import logging
import queue
import threading

import betfairlightweight

# setup logging
logging.basicConfig(level=logging.INFO)  # change to DEBUG to see log all updates

# create trading instance (app key must be activated for cricket stream)
trading = betfairlightweight.APIClient("username", "password", app_key="appKey")

# login
trading.login()

# create queue
output_queue = queue.Queue()

# create stream listener
listener = betfairlightweight.StreamListener(output_queue=output_queue)

# create stream
stream = trading.streaming.create_stream(listener=listener, host="sports_data")

# subscribe
streaming_unique_id = stream.subscribe_to_cricket_matches()

# start stream in a new thread (in production would need err handling)
t = threading.Thread(target=stream.start, daemon=True)
t.start()

# check for updates in output queue
while True:
    updates = output_queue.get()
    for update in updates:
        print(update.json())
