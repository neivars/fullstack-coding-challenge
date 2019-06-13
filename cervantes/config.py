"""
This module defines the configuration objects used by the Flask instance
to configure itself. Flask accepts UPPERCASE attributes of a class as keys
for configuration.

    class ConfigError : Exception
        Raised when the configuration files are not accessible or hold
        invalid YAML syntax.

    function _load_config
        Private function that loads and parses the YAML configuration
        file that brings in common config values.

    class ProductionConfig
        Object that holds the Flask instance configuration for production.

    class TestingConfig
        Object that holds the Flask instance configuration for testing.
"""


import yaml


class ConfigError(Exception):
    """
    Raised when the configuration files are not accessible or hold
    invalid YAML syntax.
    """

    pass


def _load_config(config_instance, testing=False, path='cervantes.yaml'):
    """
    Returns the configuration values for Flask application instances.

        config_instance : ProductionConfig | TestingConfig
            Instance of the config classes used by the Flask instance
            to attach the config keys from the config file to.

        testing : bool
            If set to False (default), the config values for production
            are used. If set to True, the config values for testing are
            used.

        path : str = 'cervantes.yaml'
            Path to the YAML configuration file. Defaults to the
            default configuration file.

        Returns : dict
            Dictionary of config keys and their values

        Raises
            ConfigError
                Raised when something wrong happens to the finding,
                parsing and/or assignment of the config values.
    """

    try:
        with open(path, 'r') as config_file:
            cervantes_config = yaml.safe_load(config_file)['production']
            config_instance.SECRET_KEY = cervantes_config['SECRET_KEY']
            config_instance.SQLALCHEMY_DATABASE_URI = cervantes_config['SQLALCHEMY_DATABASE_URI']
    except (FileNotFoundError, yaml.YAMLError, KeyError) as exc:
        raise ConfigError('Cervantes Config File Error: {}'.format(exc))


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

    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        # Turn off Flask-SQLAlchemy custom events to save resources
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        _load_config(self)


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

    def __init__(self):
        self.DEBUG = True
        self.TESTING = True
        # Turn off Flask-SQLAlchemy custom events to save resources
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        _load_config(self, testing=True)
