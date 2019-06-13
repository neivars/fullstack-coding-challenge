from cervantes.config import ConfigError, _load_config, ProductionConfig, TestingConfig
import pytest


def test_load_config_non_existent_file_production():
    """
    Check if a ConfigError exception is raised if the config file
    does not exist.
    """

    with pytest.raises(ConfigError):
        _load_config(ProductionConfig(), path='non-existent-config-file.yaml')


def test_load_config_non_existent_file_testing():
    """
    Check if a ConfigError exception is raised if the config file
    does not exist.
    """

    with pytest.raises(ConfigError):
        _load_config(TestingConfig(), path='non-existent-config-file.yaml')
