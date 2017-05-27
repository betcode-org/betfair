from ..streaming import (
    BaseListener,
    BetfairStream,
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

    def create_stream(self, unique_id=0, listener=None, timeout=11, buffer_size=1024, description='BetfairSocket'):
        """
        Creates BetfairStream.

        :param dict unique_id: Id used to start unique id's of the stream (+1 before every request)
        :param resources.Listener listener:  Listener class to use
        :param float timeout: Socket timeout
        :param int buffer_size: Socket buffer size
        :param str description: Betfair stream description

        :rtype: resources.BetfairStream
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
        )
