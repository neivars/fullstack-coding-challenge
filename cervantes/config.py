"""
This module defines the configuration objects used by the Flask instance
to configure itself. Flask accepts UPPERCASE attributes of a class as keys
for configuration.

class ProductionConfig
    Object that holds the Flask instance configuration for production.

class TestingConfig
    Object that holds the Flask instance configuration for testing.
"""


class ProductionConfig():
    """
    Set flask.debug and flask.testing to False. The SQLAlchemy database
    URI points to the production database.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/unbabel'


class TestingConfig():
    """
    Set flask.debug and flask.testing to True. The SQLAlchemy databse
    URI points to the testing database, where tables are dropped and created
    which each test suite run.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/unbabel_testing'
