import logging

from .apiclient import APIClient
from .exceptions import BetfairError
from .streaming import StreamListener
from . import filters

__title__ = "betfairlightweight"
__version__ = "2.0.0b"
__author__ = "Liam Pauling"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
