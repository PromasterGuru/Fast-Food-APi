#instance/config.py

import os


class Config():
    """Parent class with default setting configurations"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Enable Debugging mode in Development"""
    DEBUG = True
    # DATABASE_URL = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
    """Disable Debugging and Testing mode in Production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Enable Debugging and Testing mode in Testing"""
    DEBUG = True
    TESTING = True
    # DATABASE_URL = os.getenv('DATABASE_TESTDB_URL')


class StaggingConfig(Config):
    """Enable Debugging mode in Stagging"""
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'Stagging': StaggingConfig
}
