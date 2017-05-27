from .baseresource import BaseResource


class RaceDetails(BaseResource):

    def __init__(self, **kwargs):
        super(RaceDetails, self).__init__(**kwargs)
        self.response_code = kwargs.get('responseCode')
        self.race_id = kwargs.get('raceId')
        self.meeting_id = kwargs.get('meetingId')
        self.race_status = kwargs.get('raceStatus')
        self.last_updated = self.strip_datetime(kwargs.get('lastUpdated'))


class UpdateContext(object):

    def __init__(self, lastUpdated, updateSequence, updateType, eventTime=None):
        self.last_updated = BaseResource.strip_datetime(lastUpdated)
        self.update_sequence = updateSequence
        self.update_type = updateType
        self.event_time = eventTime


class Score(BaseResource):

    def __init__(self, **kwargs):
        super(Score, self).__init__(**kwargs)
        self.event_id = kwargs.get('eventId')
        self.event_type_id = kwargs.get('eventTypeId')
        self.event_status = kwargs.get('eventStatus')
        self.response_code = kwargs.get('responseCode')
        self.update_context = UpdateContext(**kwargs.get('updateContext')) if kwargs.get('updateContext') else None
        self.values = kwargs.get('values')


# class Incident(object):
#
#     def __int__(self, updateContext, values):
#         self.update_context = updateContext
#         self.values = values


class Incidents(BaseResource):

    def __init__(self, **kwargs):
        super(Incidents, self).__init__(**kwargs)
        self.event_id = kwargs.get('eventId')
        self.event_type_id = kwargs.get('eventTypeId')
        self.event_status = kwargs.get('eventStatus')
        self.response_code = kwargs.get('responseCode')
        self.incidents = kwargs.get('incidents')


class AvailableEvent(BaseResource):

    def __init__(self, **kwargs):
        super(AvailableEvent, self).__init__(**kwargs)
        self.event_id = kwargs.get('eventId')
        self.event_type_id = kwargs.get('eventTypeId')
        self.event_status = kwargs.get('eventStatus')
