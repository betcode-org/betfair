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

# create trading instance
username = os.environ.get('username')
trading = betfairlightweight.APIClient(username)
trading.login()

# update
event_id = 28350688

# score request (provide list / returns list)
scores = trading.in_play_service.get_scores(
    event_ids=[event_id]
)
print(scores)
for score in scores:
    print(
        score,
        score.description,
        score.status,
        '%s-%s' % (score.score.home.score, score.score.away.score)
    )  # view resources or debug to see all values available


# timeline request
timeline = trading.in_play_service.get_event_timeline(
    event_id=event_id
)
print(timeline)
for update in timeline.update_detail:
    print(
        update.update_id,
        update.elapsed_regular_time,
        update.type,
        update.update_time,
    )  # view resources or debug to see all values available
