from typing import Any, Dict, List

from .__version__ import __version__
from .serverapplication import JupyterDockerExtensionApp


def _jupyter_server_extension_points() -> List[Dict[str, Any]]:
    return [{
        "module": "jupyter_docker",
        "app": JupyterDockerExtensionApp,
    }]
