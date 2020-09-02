.. :changelog:

Release History
---------------

2.8.0 (2020-09-02)
+++++++++++++++++++

**Improvements**

- Transaction count updated to 5000

**Dependencies**

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
