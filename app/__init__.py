from flask import Flask
from flask_cors import CORS

from app.logging_config import setup_logging
from app.metrics import metrics


def create_app():
    setup_logging()
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    metrics.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    return app
