"""
This module defines the configuration objects used by the Flask instance
to configure itself. Flask accepts UPPERCASE attributes of a class as keys
for configuration.

    class ConfigError : Exception
        Raised when the configuration files are not accessible or hold
        invalid YAML syntax.

    class ProductionConfig
        Object that holds the Flask instance configuration for production.

    class TestingConfig
        Object that holds the Flask instance configuration for testing.
"""


import yaml


class ConfigError(Exception):
    pass


class ProductionConfig():
    """
    Set flask.debug and flask.testing to False. The SQLAlchemy database
    URI points to the production database.

        path : str
            Path to the cervantes config file.

        Raises
            ConfigError
                When the file specified in the path argument is not
                found, contains invalid YAML or is missing necessary
                config keys.
    """

    def __init__(self, path='cervantes.yaml'):
        self.DEBUG = False
        self.TESTING = False
        # Turn off Flask-SQLAlchemy custom events to save resources
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        try:
            with open(path, 'r') as config_file:
                cervantes_config = yaml.safe_load(config_file)['production']
                self.SECRET_KEY = cervantes_config['SECRET_KEY']
                self.SQLALCHEMY_DATABASE_URI = cervantes_config['SQLALCHEMY_DATABASE_URI']
        except (FileNotFoundError, yaml.YAMLError, KeyError) as exc:
            raise ConfigError('Cervantes Config File Error: {}'.format(exc))


class TestingConfig():
    """
    Set flask.debug and flask.testing to True. The SQLAlchemy databse
    URI points to the testing database, where tables are dropped and created
    which each test suite run.

        path : str
            Path to the cervantes config file.

        Raises
            ConfigError
                When the file specified in the path argument is not
                found, contains invalid YAML or is missing necessary
                config keys.
    """

    def __init__(self, path='cervantes.yaml'):
        self.DEBUG = False
        self.TESTING = False
        # Turn off Flask-SQLAlchemy custom events to save resources
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        try:
            with open(path, 'r') as config_file:
                cervantes_config = yaml.safe_load(config_file)['testing']
                self.SECRET_KEY = cervantes_config['SECRET_KEY']
                self.SQLALCHEMY_DATABASE_URI = cervantes_config['SQLALCHEMY_DATABASE_URI']
        except (FileNotFoundError, yaml.YAMLError, KeyError) as exc:
            raise ConfigError('Cervantes Config File Error: {}'.format(exc))
