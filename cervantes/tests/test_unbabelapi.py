from flask import jsonify, Response

import cervantes.unbabelapi as unbabelapi

from .mocks.data import (
    MOCK_TRANSLATIONS,
    MOCK_NEW_TRANSLATION,
    MOCK_UPDATED_TRANSLATION,
    MOCK_NONUPDATED_TRANSLATION,
    MOCK_LANGUAGE_PAIRS,
    MOCK_UNBABELAPI_CONFIG
)
from .mocks import _returnNone, _raiseFileNotFoundError
from .mocks.unbabelapi import UnababelAPIMocks
from .mocks.translations import TranslationsMocks
from .mocks.requests import RequestsMocks

import pytest
import requests
import yaml


def test_request_language_pairs(monkeypatch):
    """
    Config is loaded, all the keys accounted for, successful HTTP
    status code returned.
    """

    EXPECTED_LANGUAGE_PAIRS = MOCK_LANGUAGE_PAIRS

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it returns successfully without
    # making an actual HTTP request
    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnResponseWithLanguagePairs)

    language_pairs = unbabelapi.request_language_pairs()

    assert EXPECTED_LANGUAGE_PAIRS == language_pairs


def test_request_language_pairs_config_error(monkeypatch):
    """Config is fails to load correctly."""
    # Monkeypatch the config file loading so it errors out
    monkeypatch.setattr(unbabelapi,
                        '_load_config', _raiseFileNotFoundError)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_language_pairs()

    # Monkeypatch the config file loading so it has missing keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnIncompleteConfig)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_language_pairs()


def test_request_language_pairs_unsuccessful_http_response(monkeypatch):
    """
    Config is loaded, all the keys accounted for, but unsuccessful
    HTTP status code returned.
    """

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it doesn't make an HTTP request
    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnUnsuccessfulResponse)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_language_pairs()


def test_request_translation(monkeypatch):
    """
    Config is loaded, all the keys accounted for, successful HTTP
    status code returned.
    """

    EXPECTED_NEW_TRANSLATION = MOCK_NEW_TRANSLATION

    INPUTS = (
        MOCK_NEW_TRANSLATION['source_language'],
        MOCK_NEW_TRANSLATION['target_language'],
        MOCK_NEW_TRANSLATION['text'],
    )

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it returns successfully without
    # making an actual HTTP request
    monkeypatch.setattr(
        requests, 'post', RequestsMocks._returnResponseWithNewTranslation)

    new_translation = unbabelapi.request_translation(*INPUTS)

    assert EXPECTED_NEW_TRANSLATION == new_translation


def test_request_translation_config_error(monkeypatch):
    """Config is fails to load correctly."""
    INPUTS = (
        MOCK_NEW_TRANSLATION['source_language'],
        MOCK_NEW_TRANSLATION['target_language'],
        MOCK_NEW_TRANSLATION['text'],
    )

    # Monkeypatch the config file loading so it errors out
    monkeypatch.setattr(unbabelapi,
                        '_load_config', _raiseFileNotFoundError)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation(*INPUTS)

    # Monkeypatch the config file loading so it has missing keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnIncompleteConfig)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation(*INPUTS)


def test_request_translation_unsuccessful_http_response(monkeypatch):
    """
    Config is loaded, all the keys accounted for, but unsuccessful
    HTTP status code returned.
    """

    INPUTS = (
        MOCK_NEW_TRANSLATION['source_language'],
        MOCK_NEW_TRANSLATION['target_language'],
        MOCK_NEW_TRANSLATION['text'],
    )

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it doesn't make an HTTP request
    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnUnsuccessfulResponse)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation(*INPUTS)


def test_request_translation_update(monkeypatch):
    """
    Config is loaded, all the keys accounted for, successful HTTP
    status code returned.
    """

    TRANSLATION_UID = 'uid0000005'
    EXPECTED_UPDATED_TRANSLATION = MOCK_UPDATED_TRANSLATION
    EXPECTED_NONUPDATED_TRANSLATION = MOCK_NONUPDATED_TRANSLATION

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it doesn't make an HTTP request
    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnResponseWithUpdatedTranslation)

    updated_translation = unbabelapi.request_translation_update(
        TRANSLATION_UID)

    assert EXPECTED_UPDATED_TRANSLATION == updated_translation

    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnResponseWithNonUpdatedTranslation)

    nonupdated_translation = unbabelapi.request_translation_update(
        TRANSLATION_UID)

    assert EXPECTED_NONUPDATED_TRANSLATION == nonupdated_translation


def test_request_translation_update_config_error(monkeypatch):
    """Config is fails to load correctly."""
    TRANSLATION_UID = 'uid0000005'

    # Monkeypatch the config file loading so it errors out
    monkeypatch.setattr(unbabelapi,
                        '_load_config', _raiseFileNotFoundError)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation_update(TRANSLATION_UID)

    # Monkeypatch the config file loading so it has missing keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnIncompleteConfig)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation_update(TRANSLATION_UID)


def test_request_translation_update_unsuccessful_http_response(monkeypatch):
    """
    Config is loaded, all the keys accounted for, but unsuccessful
    HTTP status code returned.
    """

    TRANSLATION_UID = 'uid0000005'

    # Monkeypatch the config file loading so it returns the right keys
    monkeypatch.setattr(unbabelapi,
                        '_load_config', UnababelAPIMocks._returnConfig)

    # Monkeypatch the requests object so it doesn't make an HTTP request
    monkeypatch.setattr(
        requests, 'get', RequestsMocks._returnUnsuccessfulResponse)

    with pytest.raises(unbabelapi.UnbabelAPIError):
        unbabelapi.request_translation_update(TRANSLATION_UID)


def test_load_config(tmp_path):
    """Load the Unbabel API config file."""
    YAML = (
        "UNBABEL_USERNAME: 'unbabel-username'\n"
        "UNBABEL_API_KEY: 'secret-unbabel-api-key'"
    )

    EXPECTED_CONIFG = MOCK_UNBABELAPI_CONFIG

    temp_config_file = tmp_path / 'unbabelapi.yaml'
    temp_config_file.write_text(YAML)

    assert EXPECTED_CONIFG == unbabelapi._load_config(
        path=temp_config_file)


def test_load_config_invalid_yaml(tmp_path):
    """Load the Unbabel API config file with invalid YAML syntax."""
    INVALID_YAML = (
        "UNBABEL_USER NAME: 'unbabel-username'\n"
        "   UNBABEL_API_KEY: 'secret-unbabel-api-key'"
    )

    temp_config_file = tmp_path / 'unbabelapi.yaml'
    temp_config_file.write_text(INVALID_YAML)

    with pytest.raises(yaml.YAMLError):
        unbabelapi._load_config(path=temp_config_file)


def test_load_config_non_existent_file():
    """Load a non-existent Unbabel API config file."""
    with pytest.raises(FileNotFoundError):
        unbabelapi._load_config(path='non-existent-config-file.yaml')
