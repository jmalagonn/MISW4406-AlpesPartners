import logging
import sys
from flask import Flask
from config import settings
from presentation.api import bp as api_bp
from infrastructure.db.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.register_blueprint(api_bp)
    
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
    
    with app.app_context():
        init_db()
        
    return app