"""Jupyter server config."""

c.SimpleApp1.configA = "ConfigA from file"  # type:ignore[name-defined]
c.SimpleApp1.configB = "ConfigB from file"  # type:ignore[name-defined]
c.SimpleApp1.configC = "ConfigC from file"  # type:ignore[name-defined]
c.SimpleApp1.configD = "ConfigD from file"  # type:ignore[name-defined]


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jupyter_server_favicon_config")
logger.info("!!!!!! LOADING CUSTOM JUPYTER SERVER FAVICON CONFIG !!!!!!")
