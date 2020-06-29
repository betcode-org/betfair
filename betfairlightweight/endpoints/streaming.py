import warnings

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
        file_path: str = None,
        listener: BaseListener = None,
        operation: str = "marketSubscription",
        **kwargs
    ) -> HistoricalStream:
        """
        Uses streaming listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str file_path: Path to historic betfair file
        :param BaseListener listener: Listener object
        :param str operation: Operation type

        :rtype: HistoricalStream
        """
        if file_path is None and kwargs.get("directory"):
            warnings.warn(
                "directory is deprecated; use file_path", DeprecationWarning,
            )
            file_path = kwargs.get("directory")

        listener = listener if listener else BaseListener()
        listener.register_stream(0, operation)
        return HistoricalStream(file_path, listener)

    @staticmethod
    def create_historical_generator_stream(
        file_path: str = None,
        listener: BaseListener = None,
        operation: str = "marketSubscription",
        **kwargs
    ) -> HistoricalGeneratorStream:
        """
        Uses generator listener/cache to parse betfair
        historical data:
            https://historicdata.betfair.com/#/home

        :param str file_path: Path to historic betfair file
        :param BaseListener listener: Listener object
        :param str operation: Operation type

        :rtype: HistoricalGeneratorStream
        """
        if file_path is None and kwargs.get("directory"):
            warnings.warn(
                "directory is deprecated; use file_path", DeprecationWarning,
            )
            file_path = kwargs.get("directory")

        listener = listener if listener else StreamListener()
        listener.register_stream(0, operation)
        return HistoricalGeneratorStream(file_path, listener)
