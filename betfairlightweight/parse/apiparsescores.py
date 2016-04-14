from ..parse.models import BetfairModel
from ..parse.enums import RaceStatusEnum


class RaceStatus(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(RaceStatus, self).__init__(date_time_sent, raw_response)
        self.response_code = result.get('responseCode')
        self.race_id = result.get('raceId')
        self.meeting_id = result.get('meetingId')
        self.race_status = result.get('raceStatus')
        self.last_updated = result.get('lastUpdated')

    @property
    def race_status_description(self):
        return RaceStatusEnum[self.race_status].value
