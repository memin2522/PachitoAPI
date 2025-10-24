from flask import Flask 
from flask_smorest import Api
from flask_sock import Sock

from .resources.main import blp as MainBlueprint
from .ws_routes import register_ws_routes

sock = Sock()

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "MIDDLEWARE PACHITOIA"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    api = Api(app)
    api.register_blueprint(MainBlueprint)

    sock.init_app(app)
    register_ws_routes(app)

    return app