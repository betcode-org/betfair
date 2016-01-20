# betfairlightweight

Lightweight python wrapper for Betfair API-NG

Allows all betting operations and some account operations.

Add you certificate into certs before installing.

The library can be used in a Python program as follows:

```python
from betfairlightweight import apiclient, apirequest

trading = apiclient.APIClient('username', 'password')

apirequest.login(trading)
```

where 'username' and 'password' are for your Betfair account.


```python
event_types = trading.list_event_types()
```

event_types is a list of classes containing data.