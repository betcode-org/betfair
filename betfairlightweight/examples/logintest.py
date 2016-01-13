import apirequest
from apiclient import APIClient


trading = APIClient('', '')

apirequest.login(trading)

# keep_alive(trading)

data = apirequest.list_event_types(trading, {"filter": {}})
print(data)

data = apirequest.list_event_types_parsed(trading, {"filter": {}})
print(data)


apirequest.logout(trading)
