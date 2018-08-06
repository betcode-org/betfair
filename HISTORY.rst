.. :changelog:

Release History
---------------

1.7.1 (2018-08-06)
+++++++++++++++++++

**Improvements**

-

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