"""
This module defines a Flask Blueprint to encapsulate the translation
feature of the app.

bp : flask.Blueprint
    Blueprint initialization. Routes all requests to '/translations'
    to its own routes.
"""


from flask import Blueprint, jsonify

from cervantes.models import Translation


bp = Blueprint('translations', __name__, url_prefix='/translations')


@bp.route('/')
def get_translations():
    """Return JSON response of all Translation records"""

    translations = Translation.get_all()
    serialized_translations = [t.dictify() for t in translations]

    return jsonify(serialized_translations)
