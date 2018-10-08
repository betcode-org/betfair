import json  # ujson causes issues
import logging

from .stream import (
    MarketStream,
    OrderStream,
    RaceStream,
)

logger = logging.getLogger(__name__)


class BaseListener(object):

    def __init__(self, max_latency=0.5):
        self.max_latency = max_latency

        self.connection_id = None
        self.stream = None
        self.stream_type = None  # marketSubscription/orderSubscription/raceSubscription
        self.stream_unique_id = None

    def register_stream(self, unique_id, operation):
        if self.stream is not None:
            logger.warning('[Listener: %s]: stream already registered, replacing data' % unique_id)
        self.stream_unique_id = unique_id
        self.stream_type = operation
        self.stream = self._add_stream(unique_id, operation)

    def on_data(self, raw_data):
        logger.info(raw_data)

    def snap(self, market_ids=None):
        """Returns a 'snap' of the current cache
        data.

        :param list market_ids: Market ids to return
        :return: Return List of resources
        """
        if self.stream:
            return self.stream.snap(market_ids)
        else:
            return []

    @property
    def updates_processed(self):
        if self.stream:
            return self.stream._updates_processed

    @property
    def initial_clk(self):
        if self.stream is not None:
            return self.stream._initial_clk

    @property
    def clk(self):
        if self.stream is not None:
            return self.stream._clk

    def _add_stream(self, unique_id, operation):
        logger.info('Register: %s %s' % (operation, unique_id))

    def __str__(self):
        return 'BaseListener'

    def __repr__(self):
        return '<BaseListener>'


class StreamListener(BaseListener):
    """Stream listener, processes results from socket,
    holds a stream which can hold order or market book
    caches
    """

    def __init__(self, output_queue=None, max_latency=0.5, lightweight=False):
        """
        :param Queue output_queue: Queue used to return data
        :param float max_latency: Logs warning if latency above value
        :param bool lightweight: Returns dict instead of resource
        """
        super(StreamListener, self).__init__(max_latency)
        self.output_queue = output_queue
        self.lightweight = lightweight

    def on_data(self, raw_data):
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data

        :param raw_data: Received raw data
        :return: Return False to stop stream and close connection
        """
        try:
            data = json.loads(raw_data)
        except ValueError:
            logger.error('value error: %s' % raw_data)
            return

        unique_id = data.get('id')

        if self._error_handler(data, unique_id):
            return False

        operation = data['op']
        if operation == 'connection':
            self._on_connection(data, unique_id)
        elif operation == 'status':
            self._on_status(data, unique_id)
        elif operation in ['mcm', 'ocm', 'rcm']:
            # historic data does not contain unique_id
            if self.stream_unique_id not in [unique_id, 'HISTORICAL']:
                logger.warning('Unwanted data received from uniqueId: %s, expecting: %s' %
                               (unique_id, self.stream_unique_id))
                return
            self._on_change_message(data, unique_id)

    def _on_connection(self, data, unique_id):
        """Called on collection operation

        :param data: Received data
        """
        if unique_id is None:
            unique_id = self.stream_unique_id
        self.connection_id = data.get('connectionId')
        logger.info('[Connect: %s]: connection_id: %s' % (unique_id, self.connection_id))

    @staticmethod
    def _on_status(data, unique_id):
        """Called on status operation

        :param data: Received data
        """
        status_code = data.get('statusCode')
        logger.info('[Subscription: %s]: %s' % (unique_id, status_code))

    def _on_change_message(self, data, unique_id):
        change_type = data.get('ct', 'UPDATE')

        logger.debug('[Subscription: %s]: %s: %s' % (unique_id, change_type, data))

        if change_type == 'SUB_IMAGE':
            self.stream.on_subscribe(data)
        elif change_type == 'RESUB_DELTA':
            self.stream.on_resubscribe(data)
        elif change_type == 'HEARTBEAT':
            self.stream.on_heartbeat(data)
        elif change_type == 'UPDATE':
            self.stream.on_update(data)

    def _add_stream(self, unique_id, stream_type):
        if stream_type == 'marketSubscription':
            return MarketStream(self)
        elif stream_type == 'orderSubscription':
            return OrderStream(self)
        elif stream_type == 'raceSubscription':
            return RaceStream(self)

    @staticmethod
    def _error_handler(data, unique_id):
        """Called when data first received

        :param data: Received data
        :param unique_id: Unique id
        :return: True if error present
        """
        if data.get('statusCode') == 'FAILURE':
            logger.error('[Subscription: %s] %s: %s' % (unique_id, data.get('errorCode'), data.get('errorMessage')))
            if data.get('connectionClosed'):
                return True
        if data.get('status'):
            # Clients shouldn't disconnect if status 503 is returned; when the stream
            # recovers updates will be sent containing the latest data
            logger.warning('[Subscription: %s] status: %s' % (unique_id, data['status']))

    def __str__(self):
        return 'StreamListener'

    def __repr__(self):
        return '<StreamListener>'
