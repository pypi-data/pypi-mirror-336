__version__ = "3.6.0-rc1.post1"

# path to unix socket file
SOCKET_FILE = "/run/dsf/dcs.sock"

# allowed connection per unix server
DEFAULT_BACKLOG = 4

# DSF protocol version
PROTOCOL_VERSION = 12

from . import commands, connections, http, object_model
