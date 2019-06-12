"""
This module defines a Flask Blueprint to encapsulate the translation
feature of the app.

The GET route to the '/' endpoint not only retrieves the Translation
records but also passes each pending record through the Unbabel API
to get the most updated data on the translation request. This is
deliberate - every time the listing is called, it is updated first if
needed, ensuring the user has the freshest data without having to
explicitly ask for the update on their records. If all records are
in a completed state, then no queries to the Unbabel API are made.

    bp : flask.Blueprint
        Blueprint initialization. Routes all requests to '/translations'
        to its own routes.

    Routes:
        GET '/'
            get_translations
            Update and return all Translations. Optional JSON format.
        POST '/'
            add_translation
            Request a new translation, hit the Unbabel API, and, if
            all goes well, store the new Translation in the database.
        GET '/language_pair'
            get_language_pairs
            Return all available language pairs for translation in JSON
            format.
    
    function _update_translations
        Private function in charge of taking a list of Transaction
        records and passing them to the Unbabel API for updated
        information, mutating the list with the fresh information,
        if it exists.
"""


from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template

from cervantes.models import Translation, db
import cervantes.unbabelapi as unbabelapi


bp = Blueprint('translations', __name__, url_prefix='/translations')


def _update_translations(translations=[]):
    """
    Takes a list of Translation requests and mutates each element based
    on data queried from the Unbabel API. If the data from Unbabel's API
    is fresher than the data in the database, updates the properties of
    the instance.

        translations : list<Translation>
            List of Translation instances. The UIDs are used to query
            the Unbabel API one by one. Fresh data is used to mutate
            the Translation instance.

        Returns : list<Translation>
            Return the updated list.

        Raises
            unbabelapi.UnbabelAPIError
                When the call or request to the Unbabel API fails.
    """

    for translation in translations:
        updated_translation = unbabelapi.request_translation_update(
            translation.uid)

        # Status changed? Update the original Translation record
        if translation.status != updated_translation.get('status'):
            translation.status = updated_translation.get('status')
            translation.translated_text = updated_translation.get(
                'translatedText', None)
            translation.text_length = len(
                updated_translation.get('translatedText', ''))


@bp.route('/')
def get_translations():
    """
    Retrieve Translation records, filtered by the ones that are pending,
    and query the Unbabel API for each one, updating each record that
    recieves a fresher status. Return all Translation records afterwards,
    with optional JSON formatting.

        Default
            Response : text/html
            Render and return an HTML table with the Translation records.

        /?format=json
            Response : application/json
            Returns the Translations records as a JSON array of translation
            objects.
    """

    pending_translations = Translation.get_all_pending()

    try:
        # Mutate the list elements so we can commit the DB session
        # and update the records
        _update_translations(pending_translations)
        db.session.commit()
    except unbabelapi.UnbabelAPIError as exc:
        # Something went wrong with the call to the Unbabel API, warn user
        flash('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')

    translations = Translation.get_all()

    if request.args.get('format') == 'json':
        serialized_translations = [t.dictify() for t in translations]
        return jsonify(serialized_translations)

    # If JSON wasn't requested, return a rendered HTML table with the results
    return render_template('translation_table.html', translations=translations)


@bp.route('/', methods=('POST',))
def add_translation():
    """
    Accept a translation request and hit the Unbabel API, subsequently
    storing it in the database for easier access later.

        Default
            Response : null
            Redirect back to root page.
    """

    # Input validation
    translation_input = {
        'source_lang': request.form.get('source-language', ''),
        'target_lang': request.form.get('target-language', ''),
        'text': request.form.get('text', '')
    }

    empty_keys = [key for key, value in translation_input.items()
                  if value == '']

    # Front-end validation failed, warn user that inputs are missing
    if len(empty_keys) > 0:
        flash('Please submit all required inputs!')
        return redirect(url_for('index'))

    try:
        # Before we submit the translation to the API, make sure the
        # language pair is available
        language_pairs = unbabelapi.request_language_pairs().get('objects', [])
        available_pair = False
        for language_pair in language_pairs:
            source_language = language_pair['lang_pair']['source_language']['shortname']
            target_language = language_pair['lang_pair']['target_language']['shortname']

            if (source_language == translation_input['source_lang']
                    and target_language == translation_input['target_lang']):
                # It's valid, no need to keep looking
                available_pair = True
                break

        if not available_pair:
            # We've exhausted all possible pairs - it's not available
            flash(
                'Our robots are still learning how to translate that, sorry! Try another language pair please.')
            return redirect(url_for('index'))

    except unbabelapi.UnbabelAPIError as exc:
        flash('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')

    try:
        # We have all inputs and the language pair is valid, so hit the Unbabel API
        new_translation = unbabelapi.request_translation(
            translation_input['source_lang'], translation_input['target_lang'], translation_input['text'])

        # Save the response to the DB with SQLAlchemy
        new_record = Translation(
            uid=new_translation['uid'],
            status=new_translation['status'],
            source_language=new_translation['source_language'],
            target_language=new_translation['target_language'],
            text=new_translation['text'])

        db.session.add(new_record)
        db.session.commit()
    except unbabelapi.UnbabelAPIError as exc:
        # Something went wrong with the call to the Unbabel API, warn user
        flash('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')

    return redirect(url_for('index'))


@bp.route('/language_pairs')
def get_language_pairs():
    """
    Retrieve all language pairs available through the Unbabel API in
    JSON format.

        Default
            Response : application/json
            Returns the available source / target language pairs for
            translation.
    """

    try:
        return jsonify(unbabelapi.request_language_pairs().get('objects', []))
    except unbabelapi.UnbabelAPIError as exc:
        pass
