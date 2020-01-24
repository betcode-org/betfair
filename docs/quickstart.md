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

## Data

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

>>> racing_filter = filters.market_filter(text_query="Horse Racing")
>>> results = trading.betting.list_events(
        filter=racing_filter
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

Get static market data using listMarketCatalogue:

```python
>>> racing_filter = filters.market_filter(
        event_type_ids=[7],  # filter on just horse racing
        market_countries=["GB"],  # filter on just GB countries
        market_type_codes=["WIN"],  # filter on just WIN market types
    )
>>> results = trading.betting.list_market_catalogue(
        market_projection=[
            "RUNNER_DESCRIPTION", 
            "RUNNER_METADATA", 
            "COMPETITION", 
            "EVENT", 
            "EVENT_TYPE", 
            "MARKET_DESCRIPTION", 
            "MARKET_START_TIME",
        ],
        filter=racing_filter,
        max_results=100,
    )
[<MarketCatalogue>, <MarketCatalogue>, ...
```

```python
>>> for i in results:
        print(
            "{0} {1:d}:{2:02d} {3} ({4})".format(
                i.market_id,
                i.market_start_time.hour, 
                i.market_start_time.minute, 
                i.event.venue,  
                i.description.market_type,
            )
        )

1.167697086 18:00 Kempton (PLACE)
1.167697085 18:00 Kempton (WIN)
1.167697089 18:00 Kempton (OTHER_PLACE)
1.167724518 18:20 Sam Houston Race Park (WIN)
1.167724731 18:29 Tampa Bay Downs (OTHER_PLACE)
1.167724730 18:29 Tampa Bay Downs (WIN)
1.167758596 18:30 Kempton (REV_FORECAST)
1.167756729 18:30 Kempton (MATCH_BET)
...
```

Dynamic market price request using listMarketBook

```python
>>> market_books = trading.betting.list_market_book(
        market_ids=["1.167697085"],
        price_projection=filters.price_projection(
            price_data=filters.price_data(ex_all_offers=True)
        ),
    )
```

Loop response and print marketBook data:

```python
>>> for market_book in market_books:
        print(  # prints market id, inplay?, status and total matched
            market_book.market_id,
            market_book.inplay,
            market_book.status,
            market_book.total_matched,
        )
        for runner in market_book.runners:  
            print (  # prints selection id, status, LPT and total matched
                runner.selection_id, 
                runner.status, 
                runner.last_price_traded, 
                runner.total_matched,
            )
            
1.167697085 False OPEN 230638.0
27024606 ACTIVE 2.38 147131.93
27596981 ACTIVE 3.25 52257.48
26105369 ACTIVE 9.4 15378.91
27596982 ACTIVE 21.0 8247.93
27596980 ACTIVE 24.0 2763.9
27596984 ACTIVE 40.0 1175.25
27596985 ACTIVE 38.0 1260.61
27596983 ACTIVE 70.0 1074.73
27062522 ACTIVE 85.0 1096.03
27596986 ACTIVE 320.0 251.17
```

## Place Order

!!! hint
    Order requests have limits, please review [Betfair documentation](https://developer.betfair.com/exchange-api/) for more information.

```python
>>> market_id = "1.131347484"
>>> selection_id = 12029579
>>> limit_order = filters.limit_order(
        size=2.00, price=1.01, persistence_type="LAPSE"
    )
>>> instruction = filters.place_instruction(
        order_type="LIMIT",
        selection_id=selection_id,
        side="LAY",
        limit_order=limit_order,
    )
>>> place_orders = trading.betting.place_orders(
        market_id=market_id, instructions=[instruction]  # list
    )

>>> print(place_orders.status)
>>> for order in place_orders.place_instruction_reports:
        print(
            "Status: {0}, BetId: {1}, Average Price Matched: {2}".format(
                order.status, 
                order.bet_id, 
                order.average_price_matched
            )
        )
           
SUCCESS
Status: SUCCESS, BetId: 192329047378, Average Price Matched: 0.0
```

## Update Order

```python
>>> bet_id = 192329047378
>>> instruction = filters.update_instruction(
        bet_id=bet_id, new_persistence_type="PERSIST"
    )
>>> update_order = trading.betting.update_orders(
        market_id=market_id, instructions=[instruction]
    )

>>> print(update_order.status)
>>> for order in update_order.update_instruction_reports:
        print("Status: {0}".format(order.status))

SUCCESS
Status: SUCCESS
```

## Replace Order

```python
>>> instruction = filters.replace_instruction(bet_id=bet_id, new_price=1.10)
>>> replace_order = trading.betting.replace_orders(
        market_id=market_id, instructions=[instruction]
    )

>>> print(replace_order.status)
>>> for order in replace_order.replace_instruction_reports:
        place_report = order.place_instruction_reports
        cancel_report = order.cancel_instruction_reports
        print(
            "Status: {0}, New BetId: {1}, Average Price Matched: {2}".format(
                order.status, 
                place_report.bet_id, 
                place_report.average_price_matched,
            )
        )
        
SUCCESS
Status: SUCCESS, New BetId: 192329894811, Average Price Matched: 0.0 
```

## Cancel Order

!!! hint
    Placing a cancel request with no betId will result in all orders for that market being cancelled and placing a cancel request without a marketId will result in all open orders across all markets being cancelled.

```python
>>> instruction = filters.cancel_instruction(bet_id=bet_id, size_reduction=2.00)
>>> cancel_order = trading.betting.cancel_orders(
        market_id=market_id, instructions=[instruction]
    )

>>> print(cancel_order.status)
>>> for cancel in cancel_order.cancel_instruction_reports:
        print(
            "Status: {0}, Size Cancelled: {1}, Cancelled Date: {2}".format(
                cancel.status, 
                cancel.size_cancelled, 
                cancel.cancelled_date,
            )
        )

SUCCESS
Status: SUCCESS, Size Cancelled: 2.0, Cancelled Date: 2020-01-22 18:08:57
```
