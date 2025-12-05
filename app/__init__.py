# from flask import Flask

# from .config import Config

# def create_app() -> Flask:
#     app = Flask(__name__)
#     app.config.from_object(Config())

#     # Lazy imports to avoid circular deps during app init
#     from .routes.health import bp as health_bp
#     from .routes.loans import bp as loans_bp
#     from .routes.stats import bp as stats_bp

#     app.register_blueprint(health_bp)
#     app.register_blueprint(loans_bp, url_prefix="/api")
#     app.register_blueprint(stats_bp, url_prefix="/api")

#     return app
import logging
import json
import time
from flask import Flask, request
from app.config import Config

from app.routes.health import health_bp
from app.routes.loans import bp as loans_bp
from app.routes.stats import stats_bp
from app.routes.metrics import metrics_bp


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "path": request.path if request else None,
            "method": request.method if request else None
        }
        return json.dumps(log)


def configure_logging(app):
    handler = logging.StreamHandler()
    if app.config.get("JSON_LOGS", False):
        handler.setFormatter(JSONFormatter())
        
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config.get("LOG_LEVEL", "INFO"))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    configure_logging(app)

    # Register endpoints
    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")
    app.register_blueprint(metrics_bp)

    # Metrics middleware
    from app.routes.metrics import REQUEST_COUNT, RESPONSE_TIME

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        endpoint = request.path
        method = request.method

        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        RESPONSE_TIME.labels(endpoint=endpoint).observe(time.time() - request.start_time)

        return response

    return app


