

class RaceStatus:

    def __init__(self, result):
        self.response_code = result['responseCode']
        if self.response_code == 'OK':
            self.race_id = result['raceId']
            self.meeting_id = result['meetingId']
            self.race_status = result['raceStatus']
            self.last_updated = result['lastUpdated']
