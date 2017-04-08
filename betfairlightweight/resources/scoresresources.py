from .baseresource import BaseResource


class RaceDetails(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race_details'
        attributes = {
            'responseCode': 'response_code',
            'raceId': 'race_id',
            'meetingId': 'meeting_id',
            'raceStatus': 'race_status',
            'lastUpdated': 'last_updated'
        }
        datetime_attributes = (
            'lastUpdated'
        )


class Score(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'score'
        attributes = {
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'eventStatus': 'event_status',
            'responseCode': 'response_code',
            'updateContext': 'update_context',
            'values': 'values',  # todo not sure what this is
        }


class Incidents(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'incident'
        attributes = {
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'eventStatus': 'event_status',
            'responseCode': 'response_code',
            'incidents': 'incidents',  # todo not sure what this is
        }


class AvailableEvent(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'available_event'
        attributes = {
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'eventStatus': 'event_status',
        }
