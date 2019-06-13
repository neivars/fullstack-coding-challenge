"""
This module is the namespace for the mocking functionality associated
with the cervantes.translations module.

    class TranslationsMocks
        Namespace for static methods. These methods are used to stub
        out functionality from the recervantes.translations module.
"""

from .data import (
    MOCK_LANGUAGE_PAIRS,
    MOCK_NEW_TRANSLATION,
    MOCK_UPDATED_TRANSLATION,
    MOCK_NONUPDATED_TRANSLATION
)


class TranslationsMocks:
    """
    Static method namespace for mocks related to the
    cervantes.translations module.

        staticmethod _returnLanguagePairs
            Return a valid pair of language pairs as if requested from
            the Unbabel API.
        staticmethod _returnNewTranslation
            Return the response body of a successful new translation
            as if requested from the Unbabel API.
        staticmethod _returnUpdatedTranslation
            Return the response body of a successful updated translation
            as if requested from the Unbabel API.
        staticmethod _returnNonUpdatedTranslation
            Return a non-updated translation as if requested from the Unbabel
            API.
    """

    @staticmethod
    def _returnLanguagePairs(*args, **kwargs):
        """
        Return a valid pair of language pairs as if requested from
        the Unbabel API.
        """

        return MOCK_LANGUAGE_PAIRS

    @staticmethod
    def _returnNewTranslation(*args, **kwargs):
        """
        Return the response body of a successful new translation
        as if requested from the Unbabel API.
        """

        return MOCK_NEW_TRANSLATION

    @staticmethod
    def _returnUpdatedTranslation(*args, **kwargs):
        """
        Return the response body of a successful updated translation
        as if requested from the Unbabel API.
        """

        return MOCK_UPDATED_TRANSLATION

    @staticmethod
    def _returnNonUpdatedTranslation(*args, **kwargs):
        """
        Return a non-updated translation as if requested from the Unbabel
        API.
        """

        return MOCK_NONUPDATED_TRANSLATION
