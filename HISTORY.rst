.. :changelog:

Release History
---------------

2.20.0 (2024-03-11)
+++++++++++++++++++

**Improvements**

- #550 update create socket for py3.12
- #562 Fix utcnow deprecation for python3.12 (@synapticarbors)
- toml file added

**Dependencies**

- python 3.12 added
- ciso8601 upgraded to 2.3.1
- orjson upgraded to 3.9.13
- black upgraded to 24.2.0

2.19.1 (2023-11-06)
+++++++++++++++++++

**Improvements**

- Slack link expires

**Dependencies**

- orjson upgraded to 3.9.9
- black upgraded to 23.10.0

2.19.0 (2023-10-04)
+++++++++++++++++++

**Improvements**

- Improve performance of BaseStream.snap @petedmarsh
- Lazily evaluate log message parameters @petedmarsh

**Dependencies**

- orjson upgraded to 3.9.7

2.18.0 (2023-08-16)
+++++++++++++++++++

**Bug Fixes**

- Prevent race condition on connect/auth by reading response off socket first

**Dependencies**

- Remove python 3.7
- requests upgraded to <2.32.0
- orjson upgraded to 3.9.4
- black upgraded to 23.7.0

2.17.3 (2023-07-24)
+++++++++++++++++++

**Improvements**

- #279 Stop prepending pardir to certs path (@mzaja)

**Dependencies**

- orjson upgraded to 3.9.2

2.17.2 (2023-05-25)
+++++++++++++++++++

**Bug Fixes**

- RaceCard missing data handling

**Dependencies**

- black upgraded to 23.1.0

2.17.1 (2023-02-08)
+++++++++++++++++++

**Dependencies**

- add python 3.11 to tests
- ciso8601 upgraded to 2.3.0
- orjson upgraded to 3.8.5

2.17.0 (2022-10-21)
+++++++++++++++++++

**Improvements**

- #498 cricket API updates

**Dependencies**

- python 3.6 removed
- orjson upgraded to 3.8.0
- black upgraded to 22.10.0

2.16.7 (2022-08-16)
+++++++++++++++++++

**Improvements**

- Implement __getitem__ for bettingresources (@mberk)
- Add "modified" field to CricketIncident (@mberk)

**Dependencies**

- orjson upgraded to 3.7.12

2.16.6 (2022-07-13)
+++++++++++++++++++

**Bug Fixes**

- Missing pt added to cricket stream output

**Dependencies**

- orjson upgraded to 3.7.7
- black upgraded to 22.6.0
- requests upgraded to <2.29.0

2.16.5 (2022-05-16)
+++++++++++++++++++

**Improvements**

- Change to Login Session Expiry Time (24 to 12 hours)

**Dependencies**

- orjson upgraded to 3.6.8
- black upgraded to 22.3.0

2.16.4 (2022-03-28)
+++++++++++++++++++

**Improvements**

- #464 Change of Minimum Stake - Multiple Currencies
- streaming `running` property added
- Long description added to setup.py

2.16.3 (2022-03-24)
+++++++++++++++++++

**Improvements**

- #460 cricket breaking changes
- betcode logo added

**Bug Fixes**

- #458 handle currupt betfair pro data

2.16.2 (2022-03-21)
+++++++++++++++++++

**Improvements**

- betcode-org transfer/renames
- Cricket stream example (@mberk)

2.16.1 (2022-02-17)
+++++++++++++++++++

**Improvements**

- order cache optimisation to create resources once (5s->0.2s)

**Dependencies**

- orjson upgraded to 3.6.7

2.16.0 (2022-02-14)
+++++++++++++++++++

**Improvements**

- Cricket Stream added (@mberk)
- `race` depreciation warning added
- PYPI secret update and deploy environment added
- slack group invite updated

2.15.4 (2022-02-07)
+++++++++++++++++++

**Bug Fixes**

- Add HISTORY.rst to MANIFEST.in to fix broken release test (@synapticarbors)

2.15.3 (2022-02-07)
+++++++++++++++++++

**Improvements**

- GBP min bet / EUR min bsp liability update

**Dependencies**

- requests upgraded to <2.28.0
- black upgraded to 22.1.0
- orjson upgraded to 3.6.6

2.15.2 (2021-12-03)
+++++++++++++++++++

**Bug Fixes**

- #438 cache missing argument 'active' (@kwassmuss)

**Dependencies**

- black upgraded to 21.11b1

2.15.1 (2021-11-11)
+++++++++++++++++++

**Bug Fixes**

- Handle missing values in Going resource

**Dependencies**

- python 3.10 testing added
- black upgraded to 21.10b0

2.15.0 (2021-10-11)
+++++++++++++++++++

**Improvements**

- #426 minor calculate tv imp
- #428 OrderStream with no caching using `listener.order_updates_only` flag
- `debug` param deprecated and handled explicitly

**Bug Fixes**

- #429 update `create_req` typing

**Dependencies**

- black upgraded to 21.9b0
- orjson upgraded to 3.6.4

2.14.1 (2021-09-22)
+++++++++++++++++++

**Improvements**

- Explicit handling of debug flag in listener and depreciation warning added

2.14.0 (2021-09-16)
+++++++++++++++++++

**Improvements**

- `active` flag added to stream and cache to optimise calls in flumine when backtesting

2.13.2 (2021-08-26)
+++++++++++++++++++

**Improvements**

- currency_parameters updated

**Bug Fixes**

- Bump socket timeout to 64s to correctly raise Betfair timeouts and prevent unwanted Socket timeouts
- Split socket shutdown and close in socket.stop()
- Missing timeouts added to request endpoints

**Dependencies**

- orjson upgraded to 3.6.3

2.13.1 (2021-08-16)
+++++++++++++++++++

**Bug Fixes**

- #417 handle betfair historic data with listener flags

**Dependencies**

- orjson upgraded to 3.6.1
- ciso8601 upgraded to 2.2.0

2.13.0 (2021-08-03)
+++++++++++++++++++

**Bug Fixes**

- #396 Socket timeout set after call to connect (no thanks to @agberk)
- #403 default to StreamListener
- #411 New API Release w/c 9th August - listCurrentOrders - includeItemDescription

**Dependencies**

- black upgraded to 21.7b0

2.12.3 (2021-07-15)
+++++++++++++++++++

**Bug Fixes**

- #312 ensure exceptions are picklable (@aquasync)
- KA resources typo(@stevenwinfield)

**Dependencies**

- orjson upgraded to 3.6.0
- requests upgraded to 2.27.0

2.12.2 (2021-06-28)
+++++++++++++++++++

**Improvements**

- Upgrade to GitHub-native Dependabot

**Bug Fixes**

- Change to resources.LegacyData to make marketName non required field (@varneyo)

**Dependencies**

- orjson upgraded to 3.5.3
- black upgraded to 21.6b0

2.12.1 (2021-03-09)
+++++++++++++++++++

**Improvements**

- Allow single file (.pem) certificate (@beci)
- Tests directory cleanup

**Bug Fixes**

- #387 default total matched set to 0 (was None)
- #384 make regulator code optional in CurrentOrder
- #380 make name optional in scores

**Dependencies**

- orjson upgraded to 3.5.1

2.12.0 (2021-01-25)
+++++++++++++++++++

**Improvements**

- #373 Streaming refactor (2-3x+ speed improvement) using extensive caching of dicts/resources
- #369 Matches resource added
- Regression tests added to streaming operations

**Bug Fixes**

- SP traded fix, order wrong and wrong way around vs api/site

**Dependencies**

- orjson upgraded to 3.4.7

2.11.2 (2021-01-18)
+++++++++++++++++++

**Improvements**

- #370 Session timeout updated to 24hrs for international exchange
- License update
- Removed build.sh

**Dependencies**

- py3.5 testing removed

2.11.1 (2020-12-26)
+++++++++++++++++++

**Bug Fixes**

- #366 Parse Error in Setup.py at '_require' (@mlabour)

**Dependencies**

- orjson upgraded to 3.4.6

2.11.0 (2020-12-07)
+++++++++++++++++++

**Improvements**

- Stream updates

**Dependencies**

- orjson upgraded to 3.4.5

2.10.2 (2020-11-28)
+++++++++++++++++++

**Improvements**

- #359 Exchange Stream API Release - Tuesday 8th December – New field - cancelledDate
- Historical gen updated to only yield on data (reduces function calls in flumine)

**Dependencies**

- orjson upgraded to 3.4.4

2.10.1 (2020-11-24)
+++++++++++++++++++

**Bug Fixes**

- Historical generator fixed to only call `create_resource` once per call (huge speed improvement)

**Dependencies**

- requests upgraded to <2.26.0

2.10.0 (2020-11-02)
+++++++++++++++++++

**Improvements**

- #352 exchange stream API release (10/11/20)
- Add py3.9 actions test

**Dependencies**

- orjson upgraded to 3.4.3

2.9.2 (2020-10-26)
+++++++++++++++++++

**Improvements**

- Fix broken build from source due to missing requirements-speed.txt file (@synapticarbors)

2.9.1 (2020-10-26)
+++++++++++++++++++

**Improvements**

- #345: Improve Historic.download_file (@mberk)

**Dependencies**

- orjson and ciso8601 moved to optional requirement using `pip install betfairlightweight[speed]`

2.9.0 (2020-10-12)
+++++++++++++++++++

**Improvements**

- Fix types for list_race_details (synapticarbors)
- #340 cache removal added on old markets (8 hours closed)
- Streaming snap added to resources

**Bug Fixes**

- PR added to actions

**Dependencies**

- py3.9 added to tests
- orjson updated to 3.4.0

2.8.0 (2020-09-14)
+++++++++++++++++++

**Improvements**

- Transaction count updated to 5000
- Minor codebase cleanup

**Dependencies**

- #328 ujson migrated to orjson
- black updated to 20.8b1

2.7.2 (2020-08-03)
+++++++++++++++++++

**Improvements**

- Historical streaming cleanup (operation)

2.7.1 (2020-08-03)
+++++++++++++++++++

**Improvements**

- #325 listener.status property added

**Dependencies**

- ujson bumped to 3.1.0

2.7.0 (2020-07-27)
+++++++++++++++++++

**Improvements**

- #308 remove directory warnings / handling (breaking change)
- #318 include streaming_update in generator

**Bug Fixes**

- #320 generator reuse fix

2.6.0 (2020-07-09)
+++++++++++++++++++

**Improvements**

- Response (_response) removed from BaseResources due to potential memory leaks

**Bug Fixes**

- marketType bug fix (politics markets)

2.5.0 (2020-06-22)
+++++++++++++++++++

**Improvements**

- #308 rename directory to file_path

**Bug Fixes**

- #301 uncaught Error in list_market_book

**Dependencies**

- requests bumped to < 2.25.0

2.4.0 (2020-06-09)
+++++++++++++++++++

**Improvements**

- Github actions added

**Bug Fixes**

- #304 missing regulator auth code

**Dependencies**

- ujson upgraded from 2.0.3 to 3.0.0

2.3.1 (2020-05-12)
+++++++++++++++++++

**Improvements**

- LRUCache added to strip datetime
- NemID docs added

2.3.0 (2020-04-06)
+++++++++++++++++++

**Dependencies**

- ujson upgraded to 2.0.3
- c based libraries restricted to darwin and linux platforms only

2.2.0 (2020-03-09)
+++++++++++++++++++

**Improvements**

- #283 max_latency can now be set to None

**Dependencies**

- requests upgraded from 2.22.0 to 2.23.0
- ujson upgraded from 1.35 to 2.0.1 (updates to compat.py)

2.1.0 (2020-03-02)
+++++++++++++++++++

**Improvements**

- datetime handling added to time_range filter (@trigvi)
- connectionsAvailable handling added

**Bug Fixes**

- #273 error handling added for markets without marketDefinition
- #233 sendall used instead of send so that all data is sent (bug present since 2016!)

2.0.1 (2020-02-17)
+++++++++++++++++++

**Improvements**

- Listener.add_stream cleanup

**Bug Fixes**

- #268 CPU bug when using response.text

2.0.0 (2020-02-10)
+++++++++++++++++++

**Improvements**

- *Breaking* async removed from streaming (force user to handle thread)
- *Breaking* Description removed from 'create_stream'
- Black formatting on all files
- python 'Typing' added
- locale added to Navigation
- Certificate error messages improved
- Logging added to socket send
- __version__ file added and refactor to setup.py
- __version__ added to user agent
- raw requests Response added to objects
- elapsed_time now uses time() rather than datetime
- session can be passed to client
- streaming example with error handling and retry added
- mkdocs used for documentation

**Bug Fixes**

- #217 correct usage of ujson (refactor)
- Australia login interactive domain fixed
- Correct session timeout added for int and italy exchange

**Dependencies**

- ciso8601 upgraded from 2.0.1 to 2.1.3
- python 3 only
- python 3.8 testing added

1.10.4 (2019-10-28)
+++++++++++++++++++

**Bug Fixes**

- handicap added to LegacyData

1.10.3 (2019-09-30)
+++++++++++++++++++

**Improvements**

- Remove py3.4 support

**Bug Fixes**

- #232 RuntimeError fixed on serialize_orders
- avgPriceRaw added to LegacyData (@d3alek)

**Dependencies**

- requests upgraded / unpinned from exact version

1.10.2 (2019-09-02)
+++++++++++++++++++

**Improvements**

- OrderCache / UnmatchedOrder logic improved
- streaming_update and streaming_unique_id added to lightweight response

**Bug Fixes**

- handicap bugfix on OrderCache
- Missing closed logic added to OrderCache

1.10.1 (2019-08-12)
+++++++++++++++++++

**Improvements**

- RaceCard get_race_result function added (used by mobile app)
- Streaming generator listener now defaults to StreamListener

**Bug Fixes**

- #221 inplayservice subdomain updated (ips)
- #215 marketCatalogue no ERO data

1.10.0 (2019-05-26)
+++++++++++++++++++

**Improvements**

- #163 Historical stream generator added (no threads)

**Bug Fixes**

- #165 error handling added to closed connection
- #175 locals.copy() used to prevent OverflowError in VSCode

1.9.1 (2019-04-04)
+++++++++++++++++++

**Improvements**

- #54 listRunnerBook added to .betting

1.9.0 (2019-04-04)
+++++++++++++++++++

**Bug Fixes**

- #206 _async renamed to async_ due to camel case bug

1.8.3 (2019-02-02)
+++++++++++++++++++

**Improvements**

- Cert endpoints updated.
- License update.
- Readme update.

**Bug Fixes**

- Travis now builds py3.7!

1.8.2 (2018-11-23)
+++++++++++++++++++

**Improvements**

- Certificate url for login updated.
- publish_time_epoch added to MarketBook.
- marketDefinition added to serialise so that lightweight has it returned.

1.8.1 (2018-10-12)
+++++++++++++++++++

**Improvements**

- Str representation added to PriceSize object.

**Bug Fixes**

- RaceCard resource bug fix.

**Dependencies**

- Upgrade to requests 2.20.1 (security fix)

1.8.0 (2018-10-08)
+++++++++++++++++++

**Improvements**

- LoginInteractive endpoint added.
- User-Agent added to request headers.

**Bug Fixes**

- Error handling added to RaceCard.login()

1.7.2 (2018-08-06)
+++++++++++++++++++

**Bug Fixes**

- requirements.txt added to MANIFEST

1.7.1 (2018-08-06)
+++++++++++++++++++

**Improvements**

- Now working on py3.7!
- setup.py updated to use requirements only.
- py3.7 added to appveyor but pending travis to get their act together.
- Travis and appveyor yml cleanup.

**Bug Fixes**

- async renamed to _async in betting endpoint for py3.7

1.7.0 (2018-07-23)
+++++++++++++++++++

**Improvements**

- Better logging when market added to cache and initial socket responses.

**Bug Fixes**

- Refactor of the use of update_cache to prevent duplicate RunnerBook objects #180.
- Spanish URL updated, closes #164.

**Breaking Changes**

- async renamed to _async due to it being a reserved word in py3.7.

1.6.4 (2018-06-22)
+++++++++++++++++++

**Improvements**

- Build.sh and HISTORY.rst added

**Dependencies**

- Upgrade to ciso8601 2.0.1
- Upgrade to requests 2.19.1
