import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    MONGO_URI = os.environ.get('MONGO_TEST_URI')


class StagingConfig(BaseConfig):
    """Staging configuration"""


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGO_URI = os.environ.get('MONGO_URI')