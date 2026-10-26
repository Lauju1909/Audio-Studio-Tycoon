"""Menues: business (aufgeteilt nach Themen)."""
from .._linking import link_namespaces
from . import finance
from .finance import *  # noqa: F401,F403
from . import live_services
from .live_services import *  # noqa: F401,F403
from . import products
from .products import *  # noqa: F401,F403
from . import corporate
from .corporate import *  # noqa: F401,F403

link_namespaces([finance, live_services, products, corporate])
