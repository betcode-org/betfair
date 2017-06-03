from __future__ import print_function

import json
import logging

from .stream import (
    MarketStream,
    OrderStream,
)

logger = logging.getLogger(__name__)


class BaseListener(object):

    def __init__(self, max_latency=0.5):
        self.max_latency = max_latency

        self.stream = None
        self.stream_type = None  # marketSubscription/orderSubscription
        self.stream_unique_id = None

    def register_stream(self, unique_id, operation):
        if self.stream is not None:
            logger.warning('[Listener: %s]: stream already registered, replacing data' % unique_id)
        self.stream = self._add_stream(unique_id, operation)
        self.stream_type = operation
        self.stream_unique_id = unique_id

    def on_data(self, raw_data):
        print(raw_data)

    def _add_stream(self, unique_id, operation):
        print('Register: %s %s' % (operation, unique_id))

    def __str__(self):
        return '<BaseListener>'

    def __repr__(self):
        return str(self)


class StreamListener(BaseListener):
    """Stream listener, processes results from socket,
    holds a market or order stream which hold
    market_book caches
    """

    def __init__(self, output_queue, max_latency=0.5, lightweight=False):
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

        operation = data.get('op')
        if operation == 'connection':
            self._on_connection(data, unique_id)
        elif operation == 'status':
            self._on_status(data, unique_id)
        elif operation in ['mcm', 'ocm']:
            # historic data does not contain unique_id
            if self.stream_unique_id not in [unique_id, 'HISTORICAL']:
                logging.warning('Unwanted data received from uniqueId: %s, expecting: %s' %
                                (unique_id, self.stream_unique_id))
                return
            self._on_change_message(data, unique_id)

    def _on_connection(self, data, unique_id):
        """Called on collection operation

        :param data: Received data
        """
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
            return MarketStream(
                unique_id, self.output_queue, self.max_latency, self.lightweight
            )
        elif stream_type == 'orderSubscription':
            return OrderStream(
                unique_id, self.output_queue, self.max_latency, self.lightweight
            )

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

    def __str__(self):
        return 'StreamListener'

    def __repr__(self):
        return '<StreamListener>'
