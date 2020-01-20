# QuickStart

First, start by importing betfairlightweight:

```python
>>> import betfairlightweight
```

Now, try logging in:

```python
>>> trading = betfairlightweight.APIClient(
        "username", "password", app_key="app_key", certs="/certs"
    )
>>> trading.login()
<LoginResource>
```

If you do not have certificates setup on your account you can use the interactive login:

```python
>>> trading = betfairlightweight.APIClient(
        "username", "password", app_key="app_key"
    )
>>> trading.login_interactive()
<LoginResource>
```

!!! danger
    It is strongly recommended to use certificates combined with 2FA when logging in.


Once logged in the client stores the login time and session token:

```python
>>> trading.session_token
'ergregergreger==regregreg'

>>> trading.session_expired
False
```

Once logged in you can keep the session alive or logout:

```python
>>> trading.keep_alive()
<KeepAliveResource>

>>> trading.logout()
<LogoutResource>
```

## Betting

The client matches the API-NG by splitting the operations per endpoint, therefore in order to list all event types:

```python
>>> results = trading.betting.list_event_types()
[<EventTypeResult>, <EventTypeResult>, ...
```

The responses are parsed into python objects allowing easy use:

```python
>>> for i in results:
        print(i.event_type.id, i.event_type.name, i.market_count)

1 Soccer 2381
2 Tennis 3402
3 Golf 9
4 Cricket 380
5 Rugby Union 29
...
```

Or to list events using a market filter:

```python
>>> from betfairlightweight import filters

>>> results = trading.betting.list_events(
        filter=filters.market_filter(text_query="Horse Racing")
    )
[<EventResult>, <EventResult>, ...
```

```python
>>> for i in results:
        print(i.event.id, i.event.name, i.market_count)

29324768 Aintree 4th Apr 1
29660708 Arar (AUS) 21st Jan 14
29661349 Aque (US) 20th Jan 9
29636646 Newmarket 3rd May 1
29660974 Wolv 20th Jan 32
...
```