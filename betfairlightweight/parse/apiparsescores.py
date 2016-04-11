from betfairlightweight.parse.models import BetfairModel
from betfairlightweight.parse.enums import RaceStatusEnum


class RaceStatus(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(RaceStatus, self).__init__(date_time_sent, raw_response)
        self.response_code = result['responseCode']
        if self.response_code == 'OK':
            self.race_id = result['raceId']
            self.meeting_id = result['meetingId']
            self.race_status = result['raceStatus']
            self.last_updated = result['lastUpdated']

    @property
    def race_status_description(self):
        return RaceStatusEnum[self.race_status].value
