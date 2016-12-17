from ..streaming import BaseListener, BetfairStream


class Streaming(object):

    def __init__(self, parent):
        """
        :param parent: API client.
        """
        self.client = parent

    def create_stream(self, unique_id, listener=None, timeout=11, buffer_size=1024, description='BetfairSocket'):
        listener = listener if listener else BaseListener()
        return BetfairStream(unique_id, listener, app_key=self.client.app_key, session_token=self.client.session_token,
                             timeout=timeout, buffer_size=buffer_size, description=description)
