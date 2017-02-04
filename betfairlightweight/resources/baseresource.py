import datetime
import json

from ..compat import basestring, integer_types


class BaseResource(object):
    """
    Data structure based on a becket resource
        https://github.com/phalt/beckett
    """

    class Meta:
        identifier = 'id'  # The key with which you uniquely identify this resource.
        attributes = {'id': 'id'}  # Acceptable attributes that you want to display in this resource.
        sub_resources = {}  # sub resources are complex attributes within a resource
        datetime_attributes = ()  # Attributes to be converted to datetime

    def __init__(self, **kwargs):
        self._datetime_sent = kwargs.pop('date_time_sent', None)

        # todo, move the following to just MarketBook and CurrentOrders
        self.streaming_unique_id = kwargs.pop('streaming_unique_id', None)
        self.publish_time = kwargs.pop('publish_time', None)
        self.market_definition = kwargs.pop('market_definition', None)

        now = datetime.datetime.utcnow()
        self.datetime_created = now
        self._datetime_updated = now
        self._sub_resource_map = getattr(self.Meta, 'sub_resources', {})
        self._data = kwargs
        self.set_attributes(**kwargs)

    def set_sub_resources(self, **kwargs):
        """
        For each sub resource assigned to this resource, generate the
        sub resource instance and set it as an attribute on this instance.
        """
        for attribute_name, resource in self._sub_resource_map.items():
            sub_attr = kwargs.get(attribute_name)
            sub_attr_name = self.Meta.attributes.get(attribute_name,
                                                     resource.Meta.identifier)
            if sub_attr:
                if isinstance(sub_attr, list):
                    value = [resource(**x) for x in sub_attr]  # A list of sub resources is supported
                else:
                    value = resource(**sub_attr)  # So is a single resource
                setattr(self, sub_attr_name, value)
            else:
                setattr(self, sub_attr_name, [])  # [] = Empty resource

    def set_attributes(self, **kwargs):
        """
        Set the resource attributes from the kwargs.
        Only sets items in the `self.Meta.attributes` white list.
        Subclass this method to customise attributes.
        """
        if self._sub_resource_map:
            self.set_sub_resources(**kwargs)
            for key in self._sub_resource_map.keys():
                kwargs.pop(key, None)  # Don't let these attributes be overridden later
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                if field in self.Meta.datetime_attributes:
                    value = self.strip_datetime(value) or value
                setattr(self, self.Meta.attributes[field], value)

    def json(self):
        return json.dumps(self._data)

    @staticmethod
    def strip_datetime(value):
        """
        Converts value to datetime if string or int.
        """
        if isinstance(value, basestring):
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
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

    def __getattr__(self, item):
        """
        If item is an expected attribute in Meta
        return None, if not raise Attribute error.
        """
        if item in self.Meta.attributes.values():
            return
        else:
            return self.__getattribute__(item)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
