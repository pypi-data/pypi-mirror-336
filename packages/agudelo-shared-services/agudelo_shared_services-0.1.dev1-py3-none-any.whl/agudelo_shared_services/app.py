from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import agudelo_shared_services._version as v
from agudelo_shared_services.db import init_db, close_db


def create_app() -> Flask:
    # Initialize app
    app: Flask = Flask(__name__)

    app.logger.info("Initializing Server %s [v%s]", __name__, v.version)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1)

    from agudelo_shared_services.blueprints.api import api_v2

    app.register_blueprint(api_v2)

    app.logger.info("Initializing Database")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db, name="init_db")

    return app
