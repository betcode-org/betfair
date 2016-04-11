import datetime


class BetfairModel:

    def __init__(self, date_time_sent, raw_response):
        self.date_time_received = datetime.datetime.now()
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response

    @property
    def elapsed_time(self):
        return (self.date_time_received-self.date_time_sent).total_seconds()
