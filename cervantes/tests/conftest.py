import pytest

from cervantes import create_app
from cervantes.models import db as _db, Translation
from .mocks.data import MOCK_TRANSLATIONS


@pytest.fixture()
def app():
    """Create a Flask instance with testing config"""

    app = create_app(testing=True)
    with app.app_context():
        yield app


@pytest.fixture()
def db(app):
    """Use the connection to the test database to setup mock data"""

    _db.app = app

    # Setup tables in testing database
    _db.drop_all()
    _db.create_all()

    # Insert the mock data
    for translation in MOCK_TRANSLATIONS:
        _db.session.add(Translation(**translation))
    _db.session.commit()

    yield _db

    # Teardown tables in testing database
    _db.session.remove()
    _db.drop_all()


@pytest.fixture()
def client(app):
    """Create a test client for testing fake requests"""

    return app.test_client()
