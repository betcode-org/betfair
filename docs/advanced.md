# Advanced


### Locale

Betfair uses slightly different endpoints depending on your country of residence, these can be used by changing the locale on client initialisation:

```python
>>> trading = betfairlightweight.APIClient(
        "username", 
        "password", 
        app_key="app_key", 
        locale="italy"
    )
```

- spain
- italy
- romania
- sweden
- australia

### NEMID Login

Danish residents are restricted in how they login due to NemID requirements, this can be handled by replicating the login flow:

```python
import re
import betfairlightweight

trading = betfairlightweight.APIClient("username", "password", app_key="app_key")

resp = trading.session.post(
    url=trading.login_interactive.url,
    data={
        "username": trading.username,
        "password": trading.password,
        "redirectMethod": "POST",
        "product": trading.app_key,
        "url": "https://www.betfair.com",
        "submitForm": True,
    }
)
session_token = re.findall(
    "ssoid=(.*?);", resp.headers["Set-Cookie"]
)
trading.set_session_token(session_token[0])

print(trading.betting.list_event_types())
```

### Session

The client assumes requests is used for the http requests but other clients can be used if required, a session object can be passed to the client:

```python
>>> session = requests.session()
>>> trading = betfairlightweight.APIClient(
        "username", 
        "password", 
        app_key="app_key", 
        session=session,
    )
```
 
 or on a per requests basis:

```python
>>> trading.betting.list_event_types(
        filter=filters.market_filter(
            text_query='Horse Racing'
        ),
        session=session,
    )
```

### Response

The response object contains the following extra attributes:


```python
>>> response = trading.betting.list_event_types(
        filter=filters.market_filter(
            text_query='Horse Racing'
        ),
        session=session,
    )
```

Raw data / json response:


```python
>>> response[0]._data
{'eventType': {'id': '7', 'name': 'Horse Racing'}, 'marketCount': 328}

>>> response[0].json()
{"eventType":{"id":"7","name":"Horse Racing"},"marketCount":328}
```

Elapsed, created and updated time:

```python
>>> response[0].elapsed_time
0.14815688133239746

>>> response[0]._datetime_created
2020-01-27 09:56:32.984387

>>> response[0]._datetime_updated
2020-01-27 09:56:32.984387
```

Raw requests response object:

```python
>>> response[0]._response
<Response [200]>
```

### Lightweight

In order to return the raw json you can select lightweight on client initialization:

```python
>>> trading = betfairlightweight.APIClient(
        "username", 
        "password", 
        app_key="app_key", 
        certs="/certs", 
        lightweight=True,
    )
>>> trading.login()
{'sessionToken': 'dfgrtegreg===rgrgr', 'loginStatus': 'SUCCESS'}
```

or on a per request basis:

```python
>>> trading.betting.list_event_types(
        filter=filters.market_filter(
            text_query='Horse Racing'
        ),
        lightweight=True,
    )
[{'eventType': {'id': '7', 'name': 'Horse Racing'}, 'marketCount': 328}]
```

!!! hint
    Because lightweight means python doesn't need to create objects it can be considerably faster but harder to work with.

### Dependencies

By default betfairlightweight will install c based libraries if your os is either linux or darwin (Mac), due to difficulties in installation Windows users can install them seperatly:

```bash
pip install ciso8601=={version}
``` 
```bash
pip install ujson=={version}
``` 

!!! hint
    It is likely that visual studio will need to be installed as well. 
