"""Menues: gameplay (aufgeteilt nach Themen)."""
from .._linking import link_namespaces
from . import main
from .main import *  # noqa: F401,F403
from . import project_setup
from .project_setup import *  # noqa: F401,F403
from . import development
from .development import *  # noqa: F401,F403

link_namespaces([main, project_setup, development])
