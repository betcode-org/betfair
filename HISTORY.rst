.. :changelog:

Release History
---------------

1.10.2 (2019-08-??)
+++++++++++++++++++

**Improvements**

- OrderCache / UnmatchedOrder logic improved

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