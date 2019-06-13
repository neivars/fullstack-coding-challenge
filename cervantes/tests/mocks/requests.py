"""
This module is the namespace for the mocking functionality associated
with the requests module.

Requests docs: https://2.python-requests.org/en/master/

    class MockResponse
        Mock object that implements methods that requests.Response
        does as well. By returning this mocked object after stubbed
        HTTP calls, we can avoid hitting the network, pretend we
        did and get a Response object.

    class RequestMocks
        Namespace for static methods. These methods are used to stub
        out functionality from the requests package.
"""


import requests

from .data import (
    MOCK_LANGUAGE_PAIRS,
    MOCK_NEW_TRANSLATION,
    MOCK_UPDATED_TRANSLATION,
    MOCK_NONUPDATED_TRANSLATION
)


class MockResponse:
    """Mock response object for the requests module to return."""
    success = True
    content = {}

    def json(self, *args, **kwargs):
        return self.content

    def raise_for_status(self):
        if not self.success:
            raise requests.HTTPError


class RequestsMocks:
    """
    Static method namespace for mocks related to the
    requests module.

        staticmethod _returnUnsuccessfulResponse
            Return a mocked object that simulates a non-OK HTTP status.

        staticmethod _returnResponseWithLanguagePairs
            Return a response with mocked language pairs as content.

        staticmethod _returnResponseWithNewTranslation
            Return a response with a mocked new translation as content.

        staticmethod _returnResponseWithUpdatedTranslation
            Return a response with a mocked updated translation as content.

        staticmethod _returnResponseWithNonUpdatedTranslation
            Return a response with a mocked nonupdated translation as content.
    """

    @staticmethod
    def _returnUnsuccessfulResponse(*args, **kwargs):
        """Return a mocked object that simulates a non-OK HTTP status."""
        mock_response = MockResponse()
        mock_response.success = False
        return mock_response

    @staticmethod
    def _returnResponseWithLanguagePairs(*args, **kwargs):
        """Return a response with mocked language pairs as content."""
        mock_response = MockResponse()
        mock_response.content = MOCK_LANGUAGE_PAIRS
        return mock_response

    @staticmethod
    def _returnResponseWithNewTranslation(*args, **kwargs):
        """Return a response with a mocked new translation as content."""
        mock_response = MockResponse()
        mock_response.content = MOCK_NEW_TRANSLATION
        return mock_response

    @staticmethod
    def _returnResponseWithUpdatedTranslation(*args, **kwargs):
        """Return a response with a mocked updated translation as content."""
        mock_response = MockResponse()
        mock_response.content = MOCK_UPDATED_TRANSLATION
        return mock_response

    @staticmethod
    def _returnResponseWithNonUpdatedTranslation(*args, **kwargs):
        """Return a response with a mocked nonupdated translation as content."""
        mock_response = MockResponse()
        mock_response.content = MOCK_NONUPDATED_TRANSLATION
        return mock_response
