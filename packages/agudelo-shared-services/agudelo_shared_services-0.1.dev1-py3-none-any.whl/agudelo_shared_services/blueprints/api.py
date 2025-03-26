from flask import Blueprint
from flask_restx import Api
from agudelo_shared_services.namespaces.invoices import inv_ns

api_v2 = Blueprint("api", __name__, url_prefix="/api/v2")

api = Api(
    api_v2,
    version="2.0",
    title="API Familia Agudelo",
    description="API para sevicios compartidos de la famila Agudelo",
    doc="/doc/",
    security={"OAuth2": ["read", "write"]},
    # authorizations={
    #    "OAuth2": {
    #        "type": "oauth2",
    #        "flow": "implicit",
    #        "authorizationUrl": current_app.config.AUTHORIZATION_URL,
    #        "clientId": current_app.config.SWAGGER_UI_OAUTH_CLIENT_ID,
    #        "scopes": {"openid": "Get ID token", "profile": "Get Identity"},
    #    }
    # },
)

api.add_namespace(inv_ns)
