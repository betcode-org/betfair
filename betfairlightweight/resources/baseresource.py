import datetime
import ciso8601
import json

from ..compat import (
    basestring,
    integer_types,
)


class BaseResource(object):
    """Lightweight data structure for resources.
    """

    def __init__(self, **kwargs):
        self._datetime_sent = kwargs.pop('date_time_sent', None)
        now = datetime.datetime.utcnow()
        self.datetime_created = now
        self._datetime_updated = now
        self._data = kwargs

    def json(self):
        return json.dumps(self._data)

    @staticmethod
    def strip_datetime(value):
        """
        Converts value to datetime if string or int.
        """
        if isinstance(value, basestring):
            try:
                return ciso8601.parse_datetime_unaware(value)
            except ValueError:
                return
        elif isinstance(value, integer_types):
            try:
                return datetime.datetime.utcfromtimestamp(value / 1e3)
            except (ValueError, OverflowError, OSError):
                return

    @property
    def elapsed_time(self):
        """
        Elapsed time between datetime sent and datetime created
        """
        if self._datetime_sent:
            return (self.datetime_created-self._datetime_sent).total_seconds()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
