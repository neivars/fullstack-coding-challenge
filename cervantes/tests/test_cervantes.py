import pytest

from cervantes import create_app


def test_app_create_testing():
    """
    Create a Flask instance in testing mode and check
    the right config attributes.
    """

    app = create_app(testing=True)

    assert app.testing
    assert app.debug


def test_app_create_production():
    """
    Create a Flask instance and check
    the right config attributes.
    """

    app = create_app()

    assert not app.testing
    assert not app.debug


class TestAppViews():
    """
    Test suite for the root routes of the Flask app.
    """

    def test_index(self, client):
        """GET request to root renders the index template"""

        response = client.get('/')

        assert (
            b'<title>Cervantes - English to Spanish Translation</title>'
            in response.get_data()
        )
