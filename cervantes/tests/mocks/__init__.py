"""
This is the mocks package.
It holds all the placeholder data (mocks) and monkeypatched functionality
(stubs) used by the test suite. Pytest offers the monkeypatch fixture
out of the box (https://docs.pytest.org/en/latest/monkeypatch.html)
and is used to avoid making actual HTTP requests the Unbabel API.

    function _returnNone
        Function stub that ignores arguments and returns None.

    function _raiseFileNotFoundError
        Function sub that ignores arguments and raises the
        FileNotFoundError exception
"""


def _returnNone(*args, **kwargs):
    """
    Function stub that ignores arguments and returns None.

        Returns : None
    """
    return None


def _raiseFileNotFoundError(*args, **kwargs):
    """
    Function sub that ignores arguments and raises the
    FileNotFoundError exception

        Raises
            FileNotFoundError
                Always.
    """

    raise FileNotFoundError
