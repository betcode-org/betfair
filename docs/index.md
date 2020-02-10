<h1 align="center" style="font-size: 3rem; margin: -15px 0">
betfairlightweight
</h1>

---

<div align="center">
<p>
<a href="https://travis-ci.org/liampauling/betfair">
    <img src="https://travis-ci.org/liampauling/betfair.svg?branch=master" alt="Build Status">
</a>
<a href="https://coveralls.io/github/liampauling/betfair?branch=master">
    <img src="https://coveralls.io/repos/github/liampauling/betfair/badge.svg?branch=master" alt="Coverage">
</a>
<a href="https://pypi.python.org/pypi/betfairlightweight">
    <img src="https://badge.fury.io/py/betfairlightweight.svg" alt="Package version">
</a>
</p>
</div>

Lightweight, super fast (uses c libraries) pythonic wrapper for [Betfair API-NG](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni) allowing all betting operations (including market and order streaming) and account operations.

---

Get started...

```python
>>> import betfairlightweight
>>> trading = betfairlightweight.APIClient(
        "username", "password", app_key="app_key", certs="/certs"
    )
>>> trading.login()
```

Request all event types..

```python
>>> event_types = trading.betting.list_event_types()
>>> event_types
[<EventTypeResult>, <EventTypeResult>, ..]
```

## Endpoints

- trading.[login](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login)
- trading.[login_interactive](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Interactive+Login+-+API+Endpoint)
- trading.[keep_alive](https://docs.developer.betfair.com/pages/viewpage.action?pageId=3834909#Login&SessionManagement-KeepAlive)
- trading.[logout](https://docs.developer.betfair.com/pages/viewpage.action?pageId=3834909#Login&SessionManagement-Logout)

- trading.[betting](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Betting+API)
- trading.[account](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Accounts+API)
- trading.[navigation](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Navigation+Data+For+Applications)
- trading.[scores](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Race+Status+API)
- trading.[streaming](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API)
- trading.[historical](https://historicdata.betfair.com/#/apidocs)

- trading.in_play_service
- trading.race_card

!!! warning
    in_play_service and race_card are not public endpoints so may break, they are used by the betfair.com website.

## Dependencies

betfairlightweight relies on these libraries:

* `requests` - HTTP support.
* `ciso8601` - C based datetime parsing.
* `ujson` - C based json parsing.

## Installation

Install with pip:

```shell
$ pip install betfairlightweight
```

betfairlightweight requires Python 3.5+
