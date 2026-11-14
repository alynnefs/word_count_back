import logging
import os
import time
import uuid

from flask import Flask, g, request
from flask_cors import CORS

from app.logging_config import setup_logging
from app.metrics import metrics

logger = logging.getLogger(__name__)


def create_app():
    setup_logging()
    app = Flask(__name__)

    FRONTEND_URL = (
        os.environ.get("FRONTEND_URL", "http://localhost:8080")
        .strip()
        .rstrip("/")
    )
    CORS(app, origins=[FRONTEND_URL])

    metrics.init_app(app)

    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        duration_ms = round((time.time() - g.start_time) * 1000, 2)
        logger.info(
            "request",
            extra={
                "request_id": g.request_id,
                "route": request.path,
                "method": request.method,
                "status": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response

    from app.routes import bp
    app.register_blueprint(bp)

    return app
