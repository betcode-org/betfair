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

    def __init__(self, **kwargs):
        self.date_time_sent = kwargs.pop('date_time_sent', None)
        self.date_time_created = datetime.datetime.now()
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
                setattr(self, self.Meta.attributes[field], value)

    def __getattr__(self, item):
        """
        If item is an expected attribute in Meta
        return None, if not raise Attribute error.
        """
        if item in self.Meta.attributes.values():
            return
        else:
            return self.__getattribute__(item)

    @property
    def elapsed_time(self):
        if self.date_time_sent:
            return (self.date_time_created-self.date_time_sent).total_seconds()
