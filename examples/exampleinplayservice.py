import logging

import betfairlightweight

"""
inplayservice is the API endpoint that the website uses to
provide scores data, scores provides a snapshot whereas event
timeline will give update details.
"""

# setup logging
logging.basicConfig(level=logging.INFO)  # change to DEBUG to see log all updates

# create trading instance
trading = betfairlightweight.APIClient("username", "password", app_key="appKey")

# login
trading.login()

# update
event_ids = [28369618]

# score request (provide list / returns list)
scores = trading.in_play_service.get_scores(event_ids=event_ids)
print(scores)
for score in scores:
    print(
        score,
        score.description,
        score.status,
        f"{score.score.home.score}-{score.score.away.score}",
    )


# timeline request (single)
timeline = trading.in_play_service.get_event_timeline(event_id=event_ids[0])
print(timeline)
for update in timeline.update_detail:
    print(
        update.update_id, update.elapsed_regular_time, update.type, update.update_time
    )  # view resources or debug to see all values available


# timelines request (provide list / returns list)
timelines = trading.in_play_service.get_event_timelines(event_ids=event_ids)
print(timelines)
for timeline in timelines:
    for update in timeline.update_detail:
        print(
            update.update_id,
            update.elapsed_regular_time,
            update.type,
            update.update_time,
        )  # view resources or debug to see all values available
