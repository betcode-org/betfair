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
