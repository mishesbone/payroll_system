import os
import secrets
import logging
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

class Config:
    """Base configuration with common settings."""

    # 🔐 Security
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # 🔄 Flask App Settings
    FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('DEBUG') == 'True'
    
    # 📦 Database Configuration
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin@localhost:3061/pms"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # 📧 Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@payroll.com')

    # 🔄 Celery (Background Tasks)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # 🧠 AI Model Configurations
    AI_MODEL_PATH = os.environ.get('AI_MODEL_PATH', 'agentic/models/')
    NLP_MODEL_NAME = os.environ.get('NLP_MODEL_NAME', 'distilbert-base-uncased')
    PREDICTIVE_MODEL_PATH = os.environ.get('PREDICTIVE_MODEL_PATH', 'agentic/models/predictive_model.pkl')

    # 📂 File Upload Settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

    # 📜 Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')

    logging.basicConfig(
        filename=LOG_FILE,
        level=LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


class DevelopmentConfig(Config):
    """Development environment settings."""
    DEBUG = True


class TestingConfig(Config):
    """Testing environment settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory DB for faster tests
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """Production environment settings."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/payroll')


# 🔄 Configuration Dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


def get_config():
    """Retrieve the appropriate configuration based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)

