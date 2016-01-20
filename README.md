# betfairlightweight

Lightweight python wrapper for Betfair API-NG allowing all betting operations and some account operations.

Add you certificate into certs before installing.

The library can then be used in as follows:

```python
from betfairlightweight import apiclient, apirequest

trading = apiclient.APIClient('username', 'password')

apirequest.login(trading)
```


```python
event_types = trading.list_event_types()
```

event_types is a list of classes containing data.