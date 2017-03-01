"""
Application configuration
"""
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Configuration"""

    DEBUG = False
    SECRET_KEY = os.environ.get('CUSTOMER_INFO_APP_SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class ProdConfig(Config):
    """Production Configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get('CUSTOMER_INFO_APP_DATABASE')


class DevConfig(Config):
    """Development Configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
