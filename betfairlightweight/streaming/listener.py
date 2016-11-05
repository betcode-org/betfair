import json
import logging
import time

from .stream import Stream


class BaseListener:

    def __init__(self):
        self.streams = {}
        self.market_stream = None
        self.order_stream = None

    def register_stream(self, unique_id, operation):
        print('Register:', unique_id, operation)

    def on_data(self, raw_data, unique_id=None):
        print(unique_id, raw_data)


class StreamListener(BaseListener):
    """Stream listener, processes results from unlimited amount
     of sockets, holds streams which hold market_book caches
    """

    def __init__(self, output_queue=None):
        super(StreamListener, self).__init__()
        self.output_queue = output_queue

    def register_stream(self, unique_id, operation):
        if operation in ['marketSubscription', 'orderSubscription']:
            if self.streams.get(unique_id):
                logging.warning('[Listener: %s]: Stream already registered, removing data' % unique_id)
                del self.streams[unique_id]
            else:
                self._add_stream(unique_id, operation)

    def on_data(self, raw_data, unique_id=None):
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data

        :param raw_data: Received raw data
        :param unique_id: Unique id, used only on initial connection
        :return: Return False to stop stream and close connection
        """
        try:
            data = json.loads(raw_data)
        except ValueError:
            logging.error('value error: %s' % raw_data)
            return
        if not unique_id:
            unique_id = data.get('id')
        if self._error_handler(data, unique_id):
            return False

        operation = data.get('op')
        if operation == 'connection':
            self._on_connection(data, unique_id)
        elif operation == 'status':
            self._on_status(data, unique_id)
        elif operation == 'mcm' or operation == 'ocm':
            self._on_change_message(data, unique_id)
        else:
            logging.error('[Listener: %s]: Response error: %s' % (unique_id, data))

    def _on_connection(self, data, unique_id):
        """Called on collection operation

        :param data: Received data
        """
        self.connection_id = data.get('connectionId')
        logging.info('[Connect: %s]: connection_id: %s' % (unique_id, self.connection_id))

    @staticmethod
    def _on_status(data, unique_id):
        """Called on status operation

        :param data: Received data
        """
        status_code = data.get('statusCode')
        logging.info('[Subscription: %s]: %s' % (unique_id, status_code))

    def _on_change_message(self, data, unique_id):
        change_type = data.get('ct', 'UPDATE')
        stream = self.streams.get(unique_id)
        operation = data.get('op')
        if not stream:
            logging.error('[Listener: %s]: Stream not registered' % unique_id)

        logging.debug('[Subscription: %s]: %s: %s' % (unique_id, change_type, data))

        if change_type == 'SUB_IMAGE':
            stream.on_subscribe(data, operation)
        elif change_type == 'RESUB_DELTA':
            stream.on_resubscribe(data)
        elif change_type == 'HEARTBEAT':
            stream.on_heartbeat(data)
        elif change_type == 'UPDATE':
            stream.on_update(data, operation)

    def _add_stream(self, unique_id, stream_type):
        self.streams[unique_id] = Stream(unique_id, stream_type, self.output_queue)
        return self.streams[unique_id]

    @staticmethod
    def _error_handler(data, unique_id):
        """Called when data first received

        :param data: Received data
        :param unique_id: Unique id
        :return: True if error present
        """
        status_code = data.get('statusCode')
        connection_closed = data.get('connectionClosed')
        if status_code == 'FAILURE':
            logging.error('[Subscription: %s] %s: %s' %
                          (unique_id, data.get('errorCode'), data.get('errorMessage')))
            if connection_closed:
                time.sleep(1)
                return True
