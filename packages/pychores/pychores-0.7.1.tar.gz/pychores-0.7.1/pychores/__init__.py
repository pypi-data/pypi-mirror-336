"""
A flask app to help you manage your recurent tasks

I tried to use flak, sqlalchemy and pytest as cleanly as possible
This app is also a test about publishing a package using flit
"""

from flask import Flask, jsonify
from flask_cors import CORS

from ._version import version
from .configmodule import Config
from .model import DeferedSession
from .routes.auth import ClientCredsTokenValidator, DummyValidator, require_auth

__version__ = version


def respond_success(title, content):
    response_object = {
        "status": "success",
        title: content,
    }
    return jsonify(response_object)


def create_app(environment):
    app = Flask(__name__, static_folder="app", static_url_path="/")
    config = Config.get_config(environment)
    app.config.from_object(config)
    app.db_session = DeferedSession.get_session_local(
        app.config["SQLALCHEMY_DATABASE_URI"]
    )

    CORS(app, resources={r"/*": {"origins": "*"}})
    if environment == "test":
        validator = DummyValidator()
    else:
        validator = ClientCredsTokenValidator(config.KEYCLOAK_ISSUER)
    require_auth.register_token_validator(validator)

    # sanity check route
    @app.route("/infos", methods=["GET"])
    def api_version():
        return respond_success("version", __version__)

    @app.route("/api/config", methods=["GET"])
    def api_config():
        return respond_success(
            "config",
            {
                "KEYCLOAK_SERVER_URL": config.KEYCLOAK_SERVER_URL,
                "KEYCLOAK_REALM_NAME": config.KEYCLOAK_REALM_NAME,
                "KEYCLOAK_CLIENT_ID": config.KEYCLOAK_CLIENT_ID,
            },
        )

    from .routes import chores, tasks

    app.register_blueprint(tasks.bp)
    app.register_blueprint(chores.bp)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        print("catch all")
        return app.send_static_file("index.html")

    return app
