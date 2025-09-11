import logging, sys
from flask import Flask
from routes import bp as api_bp
from errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    
    # Logging configuration
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    ))
    handler.setLevel(logging.INFO)              
    app.logger.handlers = [handler]             
    app.logger.setLevel(logging.INFO)           
    app.logger.propagate = False                

    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger.handlers:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.propagate = False

    app.logger.info("Flask app logger configured at INFO")

    app.config.from_mapping(
        AFFILIATES_API_URL=os.environ.get("AFFILIATES_API_URL", "default_value"),
        LOYALTY_API_URL=os.environ.get("LOYALTY_API_URL", "default_value"),
        ALLIANCES_API_URL=os.environ.get("ALLIANCES_API_URL", "default_value"),
        DEFAULT_TIMEOUT=float(os.environ.get("DEFAULT_TIMEOUT", "2.0")),
    )

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

import os 
