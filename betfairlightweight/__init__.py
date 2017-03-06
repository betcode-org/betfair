import logging

from .apiclient import APIClient
from .exceptions import BetfairError
from .filters import MarketFilter, StreamingMarketFilter, StreamingMarketDataFilter
from .streaming import StreamListener


__title__ = 'betfairlightweight'
__version__ = '0.9.9'
__author__ = 'Liam Pauling'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
