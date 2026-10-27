# Flask Application Factory (Monolithic 3-Tier Application)
import os
from flask import Flask
from .config import config_by_name
from .models import db
from .services import TelemetryService
from .routes import web_bp, api_v1_bp, ai_agents_bp

def create_app(config_name=None):
    """Factory creating and configuring the 3-Tier Flask Application."""
    if not config_name:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static")
    )
    
    app_config = config_by_name.get(config_name, config_by_name["development"])
    app.config.from_object(app_config)

    # Initialize Tier 3 (Database ORM)
    db.init_app(app)

    # Initialize Telemetry (Azure Application Insights)
    TelemetryService.init_telemetry(app)

    # Register Blueprints (Tier 1 & 2)
    app.register_blueprint(web_bp)
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
    app.register_blueprint(ai_agents_bp, url_prefix="/api/v1/ai")

    with app.app_context():
        # Create database tables if they do not exist
        db.create_all()

    return app
