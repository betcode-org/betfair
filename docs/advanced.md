# Advanced

### Session

The client assumes requests is used for the http requests but other clients can be used if required. A session object can be passed to the client:

```python
>>> session = requests.session()
>>> trading = betfairlightweight.APIClient(
        "username", 
        "password", 
        app_key="app_key", 
        certs="/certs", 
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
