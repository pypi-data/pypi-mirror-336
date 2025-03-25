# pylint: disable=W0401,F405
"""
smarter-api local settings.
"""

from .base import *  # noqa

for handler in logging.root.handlers:
    handler.setLevel(logging.DEBUG)
