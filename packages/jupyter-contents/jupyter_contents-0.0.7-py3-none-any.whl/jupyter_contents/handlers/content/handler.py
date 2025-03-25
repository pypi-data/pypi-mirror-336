"""Content handler."""

import tornado

from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin

from ...__version__ import __version__


# pylint: disable=W0223
class ContentHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the content."""

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        """Returns the content."""
        pass
