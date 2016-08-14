import datetime


class BaseResource:
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
        self.datetime_sent = kwargs.pop('date_time_sent', None)
        self.datetime_created = datetime.datetime.utcnow()
        self.datetime_updated = datetime.datetime.utcnow()
        self._sub_resource_map = getattr(self.Meta, 'sub_resources', {})
        self.set_attributes(**kwargs)

    def set_sub_resources(self, **kwargs):
        """
        For each sub resource assigned to this resource, generate the
        sub resource instance and set it as an attribute on this instance.
        """
        for attribute_name, resource in self._sub_resource_map.items():
            sub_attr = kwargs.get(attribute_name)
            if sub_attr:
                if isinstance(sub_attr, list):
                    value = [resource(**x) for x in sub_attr]  # A list of sub resources is supported
                else:
                    value = resource(**sub_attr)  # So is a single resource
                setattr(self, resource.Meta.identifier, value)
            else:
                setattr(self, resource.Meta.identifier, None)

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

    @staticmethod
    def strip_datetime(value):
        """
        Converts value to datetime if string or int.
        """
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            except TypeError:
                return
            except ValueError:
                return
        elif isinstance(value, int):
            try:
                return datetime.datetime.fromtimestamp(value / 1e3)
            except TypeError:
                return
            except ValueError:
                return

    @property
    def elapsed_time(self):
        """
        Elapsed time between datetime sent and datetime created
        """
        if self.datetime_sent:
            return (self.datetime_created-self.datetime_sent).total_seconds()

    def __getattr__(self, item):
        """
        If item is an expected attribute in Meta
        return None, if not raise Attribute error.
        """
        if item in self.Meta.attributes.values():
            return
        else:
            return self.__getattribute__(item)

    def __str__(self):
        return self.__class__.__name__
