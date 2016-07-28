from .baseresource import BaseResource


class EventType(BaseResource):
    class Meta:
        identifier = 'event_type'
        attributes = {'id': 'id',
                      'name': 'name'}


class EventTypes(BaseResource):
    class Meta:
        identifier = 'event_type'
        attributes = {'marketCount': 'market_count'}
        sub_resources = {'eventType': EventType}
