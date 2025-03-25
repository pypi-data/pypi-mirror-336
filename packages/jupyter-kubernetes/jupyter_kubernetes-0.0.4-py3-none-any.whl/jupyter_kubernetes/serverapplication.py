"""The Jupyter Kubernetes Server application."""

import os

from traitlets import default, CInt, Instance, Unicode
from traitlets.config import Configurable

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from .__version__ import __version__

from .handlers.index.handler import IndexHandler
from .handlers.config.handler import ConfigHandler
from .handlers.kubernetes.handler import (
    PodsHandler, ServicesHandler,
)
from .handlers.echo.handler import WsEchoHandler
from .handlers.relay.handler import WsRelayHandler
from .handlers.proxy.handler import WsProxyHandler
from .handlers.ping.handler import WsPingHandler


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")


class JupyterKubernetesExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Jupyter Kubernetes Server extension."""

    name = "jupyter_kubernetes"

    extension_url = "/jupyter_kubernetes"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]

    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    class Launcher(Configurable):
        """Jupyter Kubernetes launcher configuration"""

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
            "Jupyter Kubernetes",
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
        return JupyterKubernetesExtensionApp.Launcher(parent=self, config=self.config)


    def initialize_settings(self):
        self.log.debug("Jupyter Kubernetes Config {}".format(self.config))

    def initialize_templates(self):
        self.serverapp.jinja_template_vars.update({"jupyter_kubernetes_version" : __version__})

    def initialize_handlers(self):
        handlers = [
            ("jupyter_kubernetes", IndexHandler),
            (url_path_join("jupyter_kubernetes", "config"), ConfigHandler),
            (url_path_join("jupyter_kubernetes", "echo"), WsEchoHandler),
            (url_path_join("jupyter_kubernetes", "relay"), WsRelayHandler),
            (url_path_join("jupyter_kubernetes", "proxy"), WsProxyHandler),
            (url_path_join("jupyter_kubernetes", "ping"), WsPingHandler),
            (url_path_join("jupyter_kubernetes", "pods"), PodsHandler),
            (url_path_join("jupyter_kubernetes", "services"), ServicesHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterKubernetesExtensionApp.launch_instance
