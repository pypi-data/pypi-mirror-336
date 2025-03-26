import asyncio
import os
from agudelo_shared_services.app import create_app
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
from agudelo_shared_services.exceptions.server_unsupported_env_error import (
    ServerUnsupportedEnvError,
)

app = create_app()


def deploy():
    mode = os.environ.pop("APP_ENV", "dev")

    if mode in [
        "dev",
        "qc",
        "test",
    ]:
        app.run("127.0.0.1", port=18081, debug=True)
    elif mode == "pdn":
        app_asgi = WsgiToAsgi(app)
        config = Config()
        config.bind = ["localhost:4000"]
        asyncio.run(serve(app_asgi, config))
    else:
        raise ServerUnsupportedEnvError(f"Mode {mode} is not available")
