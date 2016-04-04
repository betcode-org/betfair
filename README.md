# betfairlightweight

Lightweight python wrapper for Betfair API-NG allowing all betting operations and some account operations.

Add your certificates to '/certs/' and app_key to environment variables with username as key before installing.

.bash_profile
```
# betfair
export username = "appkey"
```

The library can then be used as follows:

```python
import betfairlightweight

trading = betfairlightweight.APIClient('username', 'password')

betfairlightweight.login(trading)
```


```python
event_types = trading.list_event_types()
```

event_types is a list of classes containing data.

# todo

    - Fix issue with no errorCode in cancel request
    - Use schematics for json -> data structure
    - Enums for correct values to be sent
    - Remove handling of expired sessionToken, should be done in framework
    - Choose where certs are located