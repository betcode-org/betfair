import logging

from .apiclient import APIClient
from .exceptions import BetfairError
from .streaming import StreamListener
from . import filters

__title__ = 'betfairlightweight'
__version__ = '1.3.1'
__author__ = 'Liam Pauling'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
