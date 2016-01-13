import apimethod
from apiclient import APIClient


trading = APIClient('', '')

apimethod.login(trading)

# keep_alive(_rcl).call()

data = apimethod.list_event_types(trading, {"filter": {}})
print(data)


print(apimethod.get_account_funds(trading, {}))
# ParameterFactory