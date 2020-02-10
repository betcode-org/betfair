import logging

from .apiclient import APIClient
from .exceptions import BetfairError
from .streaming import StreamListener
from . import filters
from .__version__ import __title__, __version__, __author__

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
