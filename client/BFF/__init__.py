from flask import Flask
from .routes import bp as api_bp
from .errors import register_error_handlers

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        AFFILIATES_SVC_URL=os.environ.get("AFFILIATES_SVC_URL", "default_value"),
        LOYALTY_SVC_URL=os.environ.get("LOYALTY_SVC_URL", "default_value"),
        ALLIANCES_SVC_URL=os.environ.get("ALLIANCES_SVC_URL", "default_value"),
        DEFAULT_TIMEOUT=float(os.environ.get("DEFAULT_TIMEOUT", "2.0")),
    )

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

import os 
