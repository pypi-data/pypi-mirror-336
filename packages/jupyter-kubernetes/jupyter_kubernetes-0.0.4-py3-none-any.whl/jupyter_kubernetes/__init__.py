from typing import Any, Dict, List

from .__version__ import __version__
from .serverapplication import JupyterKubernetesExtensionApp


def _jupyter_server_extension_points() -> List[Dict[str, Any]]:
    return [{
        "module": "jupyter_kubernetes",
        "app": JupyterKubernetesExtensionApp,
    }]


def _jupyter_labextension_paths() -> List[Dict[str, str]]:
    return [{
        "src": "labextension",
        "dest": "@datalayer/jupyter-kubernetes"
    }]
