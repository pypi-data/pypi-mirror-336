"""The Jupyter Contents Server application."""

import os

from traitlets import default, CInt, Instance, Unicode
from traitlets.config import Configurable

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from .__version__ import __version__

from .handlers.index.handler import IndexHandler
from .handlers.config.handler import ConfigHandler
from .handlers.content.handler import ContentHandler
from .handlers.echo.handler import WsEchoHandler
from .handlers.relay.handler import WsRelayHandler
from .handlers.proxy.handler import WsProxyHandler
from .handlers.ping.handler import WsPingHandler


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")


class JupyterContentsExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Jupyter Contents Server extension."""

    name = "jupyter_contents"

    extension_url = "/jupyter_contents"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    class Launcher(Configurable):
        """Jupyter Contents launcher configuration"""

        def to_dict(self):
            return {
                "category": self.category,
                "name": self.name,
                "icon_svg_url": self.icon_svg_url,
                "rank": self.rank,
            }

        category = Unicode(
            "Datalayer",
            config=True,
            help=("Application launcher card category."),
        )

        name = Unicode(
            "Jupyter Contents",
            config=True,
            help=("Application launcher card name."),
        )

        icon_svg_url = Unicode(
            None,
            allow_none=True,
            config=True,
            help=("Application launcher card icon."),
        )

        rank = CInt(
            0,
            config=True,
            help=("Application launcher card rank."),
        )

    launcher = Instance(Launcher)

    @default("launcher")
    def _default_launcher(self):
        return JupyterContentsExtensionApp.Launcher(parent=self, config=self.config)


    def initialize_settings(self):
        self.log.debug("Jupyter Contents Config {}".format(self.config))

    def initialize_templates(self):
        self.serverapp.jinja_template_vars.update({"jupyter_contents_version" : __version__})

    def initialize_handlers(self):
        self.log.debug("Jupyter Contents Config {}".format(self.settings['jupyter_contents_jinja2_env']))
        handlers = [
            ("jupyter_contents", IndexHandler),
            (url_path_join("jupyter_contents", "config"), ConfigHandler),
            (url_path_join("jupyter_contents", "content"), ContentHandler),
            (url_path_join("jupyter_contents", "echo"), WsEchoHandler),
            (url_path_join("jupyter_contents", "relay"), WsRelayHandler),
            (url_path_join("jupyter_contents", "proxy"), WsProxyHandler),
            (url_path_join("jupyter_contents", "ping"), WsPingHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterContentsExtensionApp.launch_instance
