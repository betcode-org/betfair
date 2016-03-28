from betfairlightweight.parse.meta import RACE_STATUS


class RaceStatus:

    def __init__(self, date_time_sent, raw_response, result):
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response
        self.response_code = result['responseCode']
        if self.response_code == 'OK':
            self.race_id = result['raceId']
            self.meeting_id = result['meetingId']
            self.race_status = result['raceStatus']
            self.last_updated = result['lastUpdated']

    @property
    def race_status_description(self):
        return RACE_STATUS[self.race_status]
