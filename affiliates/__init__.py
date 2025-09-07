from flask import Flask
from config import settings
from presentation.api import bp as api_bp
from infrastructure.db.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.register_blueprint(api_bp)
    
    with app.app_context():
        init_db()
        
    return app
