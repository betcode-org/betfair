from ..baseclient import BaseClient
from ..streaming import (
    BaseListener,
    StreamListener,
    BetfairStream,
    HistoricalStream,
    HistoricalGeneratorStream,
)


class Streaming:
    """
    Streaming operations.
    """

    def __init__(self, parent: BaseClient):
        """
        :param parent: API client.
        """
        self.client = parent

    def create_stream(
        self,
        unique_id: int = 0,
        listener: BaseListener = None,
        timeout: float = 11,
        buffer_size: int = 1024,
        host: str = None,
    ) -> BetfairStream:
        """
        Creates BetfairStream.

        :param int unique_id: Id used to start unique id's of the stream (+1 before every request)
        :param resources.Listener listener:  Listener class to use
        :param float timeout: Socket timeout
        :param int buffer_size: Socket buffer size
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
            host=host,
        )

    @staticmethod
    def create_historical_stream(
        directory: str, listener: BaseListener = None
    ) -> HistoricalStream:
        """
        Uses streaming listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str directory: Directory of betfair data
        :param BaseListener listener: Listener object

        :rtype: HistoricalStream
        """
        listener = listener if listener else BaseListener()
        listener.register_stream(0, "marketSubscription")
        return HistoricalStream(directory, listener)

    @staticmethod
    def create_historical_generator_stream(
        directory: str, listener: BaseListener = None
    ) -> HistoricalGeneratorStream:
        """
        Uses generator listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str directory: Directory of betfair data
        :param BaseListener listener: Listener object

        :rtype: HistoricalGeneratorStream
        """
        listener = listener if listener else StreamListener()
        listener.register_stream(0, "marketSubscription")
        return HistoricalGeneratorStream(directory, listener)
