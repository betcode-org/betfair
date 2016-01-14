import apirequest
import apiclient


trading = apiclient.APIClient('username', 'password')

apirequest.login(trading)

# keep_alive(trading)

data = apirequest.list_event_types(trading, {"filter": {}})
print(data)

data = apirequest.list_event_types_parsed(trading, {"filter": {}})
print(data)


apirequest.logout(trading)
