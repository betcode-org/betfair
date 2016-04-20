import datetime


class BetfairModel:
    """ Base class for parsing betfair response """

    def __init__(self, date_time_sent, raw_response):
        """
        :param date_time_sent:
            Datetime request sent.
        :param raw_response:
            Raw response from requests.
        """
        self.date_time_received = datetime.datetime.now()
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response

    @property
    def elapsed_time(self):
        return (self.date_time_received-self.date_time_sent).total_seconds()

    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        if str(self.raw_response) == str(other.raw_response):
            return True
