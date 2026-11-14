from pathlib import Path

from flask import redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

SPEC_DIR = Path(__file__).parent
SWAGGER_URL = "/docs"
SPEC_URL = "/openapi.yaml"


def register_docs(app):
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        SPEC_URL,
        config={"app_name": "Word Count API"},
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    @app.route(SPEC_URL)
    def openapi_spec():
        return send_from_directory(
            SPEC_DIR, "openapi.yaml", mimetype="application/yaml"
        )

    @app.route("/")
    def docs_index():
        return redirect(f"{SWAGGER_URL}/")
