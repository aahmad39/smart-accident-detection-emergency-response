# Smart Accident Detection & Emergency Response System (UK)
# Monolithic 3-Tier Architecture Configuration

import os
from datetime import timedelta

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "smart-accident-emergency-uk-dev-secret-key-2026")
    APP_NAME = "Smart Accident Detection & Emergency Response System (UK)"
    APP_VERSION = "2.4.0"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Database Configuration (Tier 3)
    # Default to SQLite for local development, easily configured for Azure SQL Database
    AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING", "")
    if AZURE_SQL_CONNECTION_STRING:
        SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={AZURE_SQL_CONNECTION_STRING}"
    else:
        # Fallback to persistent SQLite file for local dev & testing
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'accident_system.db')}")
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Azure Blob Storage Configuration (Crash Evidence & Dashcam Media)
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "crash-evidence")
    LOCAL_STORAGE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "storage_uploads")

    # Azure Application Insights & Telemetry
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")

    # Azure OpenAI Configuration (AI Agents)
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

    # UK Emergency Dispatch Service (Simulation Defaults)
    UK_EMERGENCY_SERVICE_PHONE = "999"
    DEFAULT_DISPATCH_RADIUS_KM = 25.0
    CRASH_SEVERITY_THRESHOLD_HIGH = 7.5  # G-force threshold for automatic High severity
    CRASH_SEVERITY_THRESHOLD_CRITICAL = 12.0  # G-force threshold for Critical severity

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Enforce secure cookies in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
