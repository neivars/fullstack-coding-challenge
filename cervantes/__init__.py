"""
This is the main package of the application.

    __init__.py
        This module defines an application factory that returns a Flask
        instance.

        Routes:
            GET '/'
                index
                Render the main page of the application.

    config.py
        This module defines the configuration objects used by the Flask
        instance to configure itself.

    models.py
        This module initializes the SQLAlchemy object for communicating
        with the database, and defines and registers the models that
        abstract the data.

    translations.py
        This module defines the 'translations' feature of the app as a
        Flask blueprint. Defines the routes prefixed with '/translations'.

    unbabelapi.py
        This module defines the helper methods that make calls to the
        Unbabale API.
"""


from flask import Flask, render_template

from cervantes.config import ProductionConfig, TestingConfig
from cervantes.models import db


def create_app(testing=False):
    """
    Create and return a Flask application instance.

    This instance registers the root route (/) that renders the main
    application template, and registers Flask blueprints to namespace
    and handle other application features.

    testing : bool = False
        If set to False (default), configure the Flask instance to use
        the configuration scheme for production. This will set the
        database connection to the production URI.
        If set to True, configure the Flask instance to use the
        configuration scheme for testing (with pytest). This will set
        the database connection to the test database.
    """
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(ProductionConfig())

    # Override config if testing
    if testing:
        app.config.from_object(TestingConfig())

    # Bind the SQLAlchemy database with the app
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Root level routes
    @app.route('/')
    def index():
        return render_template('index.html')

    # Blueprints for feature routes
    import cervantes.translations
    app.register_blueprint(cervantes.translations.bp)

    return app
