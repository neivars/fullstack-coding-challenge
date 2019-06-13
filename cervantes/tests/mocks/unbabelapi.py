"""
This module is the namespace for the mocking functionality associated
with the cervantes.unbabelapi module.

    class UnbabelAPIMocks
        Namespace for static methods. These methods are used to stub
        out functionality from the recervantes.unbabelapi module.
"""


from cervantes.unbabelapi import UnbabelAPIError

from .data import MOCK_UNBABELAPI_CONFIG, MOCK_INCOMPLETE_UNBABELAPI_CONFIG


class UnababelAPIMocks:
    """
    Static method namespace for mocks related to the
    cervantes.unbabelapi module.

        staticmethod _returnConfig
            Return a mocked config dict for accessing the Unbabel API.
        staticmethod _returnIncompleteConfig
            Return a mocked config dict for accessing the Unbabel API
            with missing keys.
        staticmethod _raiseUnbabelAPIError
            Raise an UnbabelAPIError.
    """

    @staticmethod
    def _returnConfig(*args, **kwargs):
        """Return a mocked config dict for accessing the Unbabel API."""
        return MOCK_UNBABELAPI_CONFIG

    @staticmethod
    def _returnIncompleteConfig(*args, **kwargs):
        """
        Return a mocked config dict for accessing the Unbabel API with
        missing keys.
        """

        return MOCK_INCOMPLETE_UNBABELAPI_CONFIG

    @staticmethod
    def _raiseUnbabelAPIError(*args, **kwargs):
        """Raise an UnbabelAPIError."""
        raise UnbabelAPIError
