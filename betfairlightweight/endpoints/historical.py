import threading

from .baseendpoint import BaseEndpoint
from ..streaming.listener import BaseListener


class Historical(BaseEndpoint):
    """
    Historical parsing/streaming.
    """

    @staticmethod
    def create_stream(directory, listener=None):
        """
        Uses streaming listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str directory: Directory of betfair data
        :param BaseListener listener: Listener object
        :rtype: HistoricalStream
        """
        listener = listener if listener else BaseListener()
        listener.register_stream('HISTORICAL', 'marketSubscription')
        return HistoricalStream(directory, listener)


class HistoricalStream(object):
    """
    Copy of 'Betfair Stream'
    """

    def __init__(self, directory, listener):
        """
        :param str directory: Directory of betfair data
        :param BaseListener listener: Listener object
        """
        self.directory = directory
        self.listener = listener

    def start(self, async=False):
        if async:
            t = threading.Thread(name='HistoricalStream', target=self._read_loop)
            t.daemon = False
            t.start()
        else:
            self._read_loop()

    def _read_loop(self):
        with open(self.directory, 'r') as f:
            for update in f:
                self.listener.on_data(update)
