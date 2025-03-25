import os
from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import FileFindHandler

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    favicon_path = os.path.join(os.path.dirname(__file__), "static", "custom", "favicons")
    
    handlers = [
        (
            url_path_join(base_url, "static/favicons/(.*)"),
            FileFindHandler,
            {'path': favicon_path}
        ),
    ]

    web_app.add_handlers(host_pattern, handlers) 
