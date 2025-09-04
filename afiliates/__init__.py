from flask import Flask
from config import settings
from presentation.api import bp as api_bp
from infrastructure.db import init_db

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = settings.DEBUG
    app.register_blueprint(api_bp)
    
    # For demo: auto-create tables (use Alembic in real apps)
    init_db()
    return app
