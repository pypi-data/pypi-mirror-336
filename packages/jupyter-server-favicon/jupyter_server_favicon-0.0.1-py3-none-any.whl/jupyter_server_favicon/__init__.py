from .handlers import setup_handlers

def _load_jupyter_server_extension(server_app):
    setup_handlers(server_app.web_app)
    name = "jupyterlab_favicon_extension"
