"""
This module is responsible for the Unbabel Translation API service.
It fetches the authorization to make calls to the Unbabel API from a
local config and defines the helper functions that make the calls to
the API in sandbox mode.

Unbabel API docs: https://developers.unbabel.com/v2/docs

    class UnbabelAPIError : Exception
        Raised when something goes wrong during the call to the
        Unbabel API.

    function _load_config
        Private function that loads and parses the YAML configuration
        file that allows access to the Unbabel API.

    function request_language_pairs
        Sends a GET request to the Unbabel API to retrieve a list
        of available source and target language pairs.

    function request_translation
        Creates and POSTs a request to the Unbabel API to request a
        new translation. Returns a Response with the result.

    function request_translation_update
        Sends a GET request with an Unbabel-generated UID to query the
        latest status of a previously requested translation.
"""


import requests
import yaml


class UnbabelAPIError(Exception):
    """Something went wrong when calling the Unbabel API."""
    pass


def _load_config(path='unbabelapi.yaml'):
    """
    Returns the configuration values to access the Unbabel API.

        path : str = 'unbabelapi.yaml'
            Path to the YAML configuration file. Defaults to the
            default configuration file.

        Returns : dict
            Dictionary of config keys and their values

        Raises
            FileNotFoundError
                When path points to a nonexistent file.
            yaml.YAMLError
                When the file being read isn't a valid YAML file or
                has syntax errors.
    """

    with open(path, 'r') as config_file:
        return yaml.safe_load(config_file)


def request_language_pairs():
    """
    Sends a GET request to the '/language_pair' Unbabel API endpoint
    and retrieves a list of the possible combinations for source and
    target languages for translation requests.

        Returns : dict
            If UnbabelAPIError is not raised, the returned dict will
            have a key 'objects' that holds a list of 'lang_pair'
            dicts representing the source and target languages
            available.

        Raises
            UnbabelAPIError
                When the call or request to the Unbabel API fails.
    """

    try:
        unbabel_config = _load_config()
    except (FileNotFoundError, yaml.YAMLError) as exc:
        raise UnbabelAPIError('API Service Config File Error: {}'.format(exc))

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey {UNBABEL_USERNAME}:{UNBABEL_API_KEY}'.format(**unbabel_config)
        }
    # Instead of a default value, that will result in a 401 response,
    # explicitly warn the user they're missing a config key and tell
    # them which one
    except KeyError as exc:
        raise UnbabelAPIError(
            'API Service Config Value Missing: {}'.format(exc))

    response = requests.get(
        'https://sandbox.unbabel.com/tapi/v2/language_pair/', headers=headers)

    # Did anything go wrong?
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise UnbabelAPIError(exc)

    # We're scot-free
    return response.json()


def request_translation(source_lang, target_lang, text):
    """
    Sends a POST request to the '/translation' Unbabel API endpoint,
    specifying the correct Authorization header format, and the
    necessary fields in the body.

        source_lang : str
            Language code of the text to the translated.
        target_land : str
            Language code of the translation.
        text : str
            Text to the translated.

        Returns : dict
            If UnbabelAPIError is not raised, the returned dict will
            be the newly created translation request, as returned by
            the Unbabel API.

        Raises
            UnbabelAPIError
                When the call or request to the Unbabel API fails.
    """

    try:
        unbabel_config = _load_config()
    except (FileNotFoundError, yaml.YAMLError) as exc:
        raise UnbabelAPIError('API Service Config File Error: {}'.format(exc))

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey {UNBABEL_USERNAME}:{UNBABEL_API_KEY}'.format(**unbabel_config)
        }
    # Instead of a default value, that will result in a 401 response,
    # explicitly warn the user they're missing a config key and tell
    # them which one
    except KeyError as exc:
        raise UnbabelAPIError(
            'API Service Config Value Missing: {}'.format(exc))

    body = {
        'text': text,
        'source_language': source_lang,
        'target_language': target_lang,
        'text_format': 'text'
    }

    response = requests.post(
        'https://sandbox.unbabel.com/tapi/v2/translation/', json=body, headers=headers)

    # Did anything go wrong?
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise UnbabelAPIError(exc)

    # We're scot-free
    return response.json()


def request_translation_update(translationId):
    """
    Sends a GET request to the '/translation/:uid' Unbabel API
    endpoint, specifying the correct Authorization header format,
    and the :uid path parameter.

        translationId : str
            List of translation request UIDs 

        Returns : dict
            If UnbabelAPIError is not raised, the returned dict will
            be the most recent data on the translation request, as
            returned by the Unbabel API.

        Raises
            UnbabelAPIError
                When the call or request to the Unbabel API fails.
    """

    try:
        unbabel_config = _load_config()
    except (FileNotFoundError, yaml.YAMLError) as exc:
        raise UnbabelAPIError('API Service Config File Error: {}'.format(exc))

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey {UNBABEL_USERNAME}:{UNBABEL_API_KEY}'.format(**unbabel_config)
        }
    # Instead of a default value, that will result in a 401 response,
    # explicitly warn the user they're missing a config key and tell
    # them which one
    except KeyError as exc:
        raise UnbabelAPIError(
            'API Service Config Value Missing: {}'.format(exc))

    response = requests.get(
        'https://sandbox.unbabel.com/tapi/v2/translation/{}'.format(
            translationId), headers=headers)

    # Did anything go wrong?
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise UnbabelAPIError(exc)

    # We're scot-free
    return response.json()
