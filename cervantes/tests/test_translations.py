from flask import get_flashed_messages, jsonify

import cervantes.translations as translations
import cervantes.unbabelapi as unbabelapi
from cervantes.models import Translation

from .mocks.data import MOCK_TRANSLATIONS, MOCK_UPDATED_TRANSLATION, MOCK_LANGUAGE_PAIRS
from .mocks import _returnNone
from .mocks.unbabelapi import UnababelAPIMocks
from .mocks.translations import TranslationsMocks

import pytest
import json
from datetime import datetime


class TestTranslationsViews():
    """
    Test suite for the Translation blueprint routes.
    URL prefix '/translations'.
    """

    def test_index_html(self, client, monkeypatch, db):
        """
        GET request to /translations returns HTML table snippet
        with data.
        """

        # Monkeypatch out the update functionality of this endpoint
        monkeypatch.setattr(translations,
                            '_update_translations', _returnNone)
        # Due to the above, monkeypatch out the database query to avoid waste
        monkeypatch.setattr(Translation, 'get_all_pending', _returnNone)

        response = client.get('/translations', follow_redirects=True)
        translationsTable = response.get_data()

        assert b'<table class="table">' in translationsTable
        assert b'<th style="width: 0">Date</th>' in translationsTable
        assert b'<th style="width: 0">Status</th>' in translationsTable
        assert b'<th style="width: 0">Source</th>' in translationsTable
        assert b'<th style="width: 0">Target</th>' in translationsTable
        assert b'<th>Text</th>' in translationsTable
        assert b'<th>Translated</th>' in translationsTable

    def test_index_json(self, client, monkeypatch, db):
        """
        GET request to /translations returns JSON table snippet
        with data.
        """

        # Monkeypatch out the update functionality of this endpoint
        monkeypatch.setattr(translations,
                            '_update_translations', _returnNone)
        # Due to the above, monkeypatch out the database query to avoid waste
        monkeypatch.setattr(Translation, 'get_all_pending', _returnNone)

        EXPECTED_IDS = ['uid0000001', 'uid0000002',
                        'uid0000003', 'uid0000004', 'uid0000005']

        response = client.get('/translations?format=json',
                              follow_redirects=True)
        all_translations = json.loads(response.get_data())

        translation_ids = [t['uid'] for t in all_translations]
        translation_ids.sort()

        assert translation_ids == EXPECTED_IDS

    def test_index_update_translations_API_error(self, client, monkeypatch):
        """
        GET request to /translations flashes a message into the session
        if the translation update Unbabel API call fails.
        """

        # Force an exception to be raised
        monkeypatch.setattr(translations,
                            '_update_translations', UnababelAPIMocks._raiseUnbabelAPIError)

        EXPECTED_FLASH = 'Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.'

        with client:
            response = client.get('/translations', follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

    def test_add_translation(self, client, monkeypatch):
        """
        POST request to /translations with valid inputs.
        """

        INPUTS = {
            'source-language': 'en',
            'target-language': 'es',
            'text': 'Example text'
        }

        # Monkeypatch a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', TranslationsMocks._returnLanguagePairs)
        # Monkeypatch a forced raise of an exception
        monkeypatch.setattr(unbabelapi,
                            'request_translation', TranslationsMocks._returnNewTranslation)

        with client:
            response = client.post(
                '/translations/', data=INPUTS, follow_redirects=True)

            assert len(get_flashed_messages()) == 0

    def test_add_translation_no_inputs_provided(self, client):
        """
        POST request to /translations with none of the required inputs.
        """

        EXPECTED_FLASH = 'Please submit all required inputs!'

        with client:
            response = client.post(
                '/translations/', data={}, follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

        with client:
            response = client.post(
                '/translations/', data={'text': 'One input at least'}, follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

    def test_add_translation_invalid_language_pair(self, client, monkeypatch):
        """
        POST request to /translations with an invalid combination of
        source-language and target-language inputs.
        """

        EXPECTED_FLASH = 'Our robots are still learning how to translate that, sorry! Try another language pair please.'

        INPUTS = {
            'source-language': 'en',
            'target-language': 'languagecodethatdefinitelydoesnotexist',
            'text': 'Example text'
        }

        # Monkeypatch a return to a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', TranslationsMocks._returnLanguagePairs)

        with client:
            response = client.post(
                '/translations/', data=INPUTS, follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

    def test_add_translation_API_error_language_pairs(self, client, monkeypatch):
        """
        POST request to /translations with valid inputs but something
        goes wrong with the Unbabel API call to request the list of
        valid language pairs.
        """

        EXPECTED_FLASH = 'Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.'

        INPUTS = {
            'source-language': 'en',
            'target-language': 'es',
            'text': 'Example text'
        }

        # Monkeypatch a forced raise of an exception
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', UnababelAPIMocks._raiseUnbabelAPIError)

        with client:
            response = client.post(
                '/translations/', data=INPUTS, follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

    def test_add_translation_API_error_request_translation(self, client, monkeypatch):
        """
        POST request to /translations with valid inputs but something
        goes wrong with the Unbabel API call to request a new
        translation.
        """

        EXPECTED_FLASH = 'Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.'

        INPUTS = {
            'source-language': 'en',
            'target-language': 'es',
            'text': 'Example text'
        }

        # Monkeypatch a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', TranslationsMocks._returnLanguagePairs)
        # Monkeypatch a forced raise of an exception
        monkeypatch.setattr(unbabelapi,
                            'request_translation', UnababelAPIMocks._raiseUnbabelAPIError)

        with client:
            response = client.post(
                '/translations/', data=INPUTS, follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()

    def test_get_language_pairs(self, client, monkeypatch):
        """
        GET request to /translations/language_pairs but something goes
        wrong with the Unbabel API call.
        """

        EXPECTED_LANGUAGE_PAIRS = MOCK_LANGUAGE_PAIRS['objects']

        # Monkeypatch a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', TranslationsMocks._returnLanguagePairs)

        response = client.get(
            '/translations/language_pairs', follow_redirects=True)

        assert EXPECTED_LANGUAGE_PAIRS == json.loads(response.get_data())

    def test_get_language_pairs_API_error(self, client, monkeypatch):
        """
        GET request to /translations/language_pairs but something goes
        wrong with the Unbabel API call.
        """

        EXPECTED_FLASH = 'Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.'

        # Monkeypatch a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_language_pairs', UnababelAPIMocks._raiseUnbabelAPIError)

        with client:
            response = client.get(
                '/translations/language_pairs', follow_redirects=True)

            assert EXPECTED_FLASH in get_flashed_messages()


class TestTranslationsHelpers():
    """
    Test suite for the Translation blueprint helper functions.
    """

    def test_update_translations_updated(self, client, monkeypatch, db):
        """
        The API gets called and the translation updated with data as
        if it came from the Unbabel API. In this test case, the data is
        fresher.
        """

        PENDING_TRANSLATIONS = Translation.get_all_pending()

        updated_translation = MOCK_TRANSLATIONS[4].copy()
        updated_translation['status'] = 'completed'
        updated_translation['translated_text'] = 'Doraemon dejame jugar'
        updated_translation['text_length'] = 21

        EXPECTED_TRANSLATIONS = [Translation(**updated_translation)]

        # Monkeypatch a valid updated translation without hitting
        # the API
        monkeypatch.setattr(unbabelapi,
                            'request_translation_update', TranslationsMocks._returnUpdatedTranslation)

        translations._update_translations(PENDING_TRANSLATIONS)

        for expected_translation, pending_translation in zip(EXPECTED_TRANSLATIONS, PENDING_TRANSLATIONS):
            assert expected_translation.dictify() == pending_translation.dictify()

    def test_update_translations_not_updated(self, client, monkeypatch, db):
        """
        The API gets called and the translation updated with data as
        if it came from the Unbabel API. In this test case, the data is
        NOT fresher.
        """

        PENDING_TRANSLATIONS = Translation.get_all_pending()

        EXPECTED_TRANSLATIONS = [Translation(**MOCK_TRANSLATIONS[4])]

        # Monkeypatch a valid nonupdated translation without hitting
        # the API
        monkeypatch.setattr(unbabelapi,
                            'request_translation_update', TranslationsMocks._returnNonUpdatedTranslation)

        translations._update_translations(PENDING_TRANSLATIONS)

        for expected_translation, pending_translation in zip(EXPECTED_TRANSLATIONS, PENDING_TRANSLATIONS):
            assert expected_translation.dictify() == pending_translation.dictify()

    def test_update_translations_API_error(self, client, monkeypatch, db):
        """
        An API error gets raised on the call to the Unbabel API to
        update the translation records.
        """

        pending_translations = Translation.get_all_pending()

        # Monkeypatch a valid language pair without hitting the API
        monkeypatch.setattr(unbabelapi,
                            'request_translation_update', UnababelAPIMocks._raiseUnbabelAPIError)

        with pytest.raises(unbabelapi.UnbabelAPIError):
            translations._update_translations(pending_translations)
