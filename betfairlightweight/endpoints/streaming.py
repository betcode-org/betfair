from ..streaming import (
    BaseListener,
    BetfairStream,
    HistoricalStream,
)


class Streaming(object):
    """
    Streaming operations.
    """

    def __init__(self, parent):
        """
        :param parent: API client.
        """
        self.client = parent

    def create_stream(self, unique_id=0, listener=None, timeout=11, buffer_size=1024, description='BetfairSocket',
                      host=None):
        """
        Creates BetfairStream.

        :param dict unique_id: Id used to start unique id's of the stream (+1 before every request)
        :param resources.Listener listener:  Listener class to use
        :param float timeout: Socket timeout
        :param int buffer_size: Socket buffer size
        :param str description: Betfair stream description
        :param str host: Host endpoint (prod (default) or integration)

        :rtype: BetfairStream
        """
        listener = listener if listener else BaseListener()
        return BetfairStream(
            unique_id,
            listener,
            app_key=self.client.app_key,
            session_token=self.client.session_token,
            timeout=timeout,
            buffer_size=buffer_size,
            description=description,
            host=host,
        )

    @staticmethod
    def create_historical_stream(directory, listener=None, operation='marketSubscription'):
        """
        Uses streaming listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str directory: Directory of betfair data
        :param BaseListener listener: Listener object
        :param str operation: Operation type

        :rtype: HistoricalStream
        """
        listener = listener if listener else BaseListener()
        listener.register_stream('HISTORICAL', operation)
        return HistoricalStream(directory, listener)
