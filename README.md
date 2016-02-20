# betfairlightweight

Lightweight python wrapper for Betfair API-NG allowing all betting operations and some account operations.

Add your certificates to '/certs/' and app_key to environment variables with username as name before installing.

.bash_profile
    export username="appkey"


The library can then be used as follows:

```python
from betfairlightweight import apiclient, apirequest

trading = apiclient.APIClient('username', 'password')

apirequest.login(trading)
```


```python
event_types = trading.list_event_types()
```

event_types is a list of classes containing data.