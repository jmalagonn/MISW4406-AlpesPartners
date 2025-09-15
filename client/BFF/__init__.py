import logging, sys
from flask import Flask
from application.routes import bp as api_bp
from domain.errors import register_error_handlers
from config import settings
from infrastructure.pulsar_ext import pulsar_ext

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    
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

    pulsar_ext.init_app(app)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @app.get("/")
    def root():
        return {"status": "ok", "message": "BFF Service is running"}, 200

    return app

import os 
