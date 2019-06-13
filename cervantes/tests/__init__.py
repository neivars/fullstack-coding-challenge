"""
This is the testing package. Testing is done through pytest.
Through the root-level config 'setup.cfg', pytest knows to look for
tests in this package.

    mocks
        This package holds all the placeholder data (mocks) and
        monkeypatched functionality (stubs) used by the test suite.
        Pytest offers the monkeypatch fixture out of the box
        (https://docs.pytest.org/en/latest/monkeypatch.html) and is
        used to avoid making actual HTTP requests the Unbabel API.

    conftest.py
        This module defines the test fixtures that are made available
        to the test cases by accepting their function names in the
        test case parameters.

    test_cervantes.py
        This module tests the cervantes (main app) package, namely the
        application factory and the routes defined directly in the
        app root.

    test_config.py
        This module tests the cervantes.config module.

    test_models.py
        This module tests the cervantes.models module.

    test_translations.py
        This module tests the cervantes.translations module.
        cervantes.translations is a blueprint, with its own helper
        functions and routes.

    test_unbabelapi.py
        This module tests the cervantes.unbabelapi.py module.
"""
