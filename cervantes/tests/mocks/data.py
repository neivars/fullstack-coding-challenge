"""
This module holds all the fake testing data (mocks) as CONSTANTS
for ease of use with the testing suite.

    MOCK_TRANSLATIONS
        Short list of Translation data that is used to seed the testing
        database.
    
    MOCK_NEW_TRANSLATION
        Example of the returned json.dumps'd body of POSTing to Unbabel
        API '/translation' endpoint.

    MOCK_UPDATED_TRANSLATION
        Example of the returned json.dumps'd body of GETing to Unbabel
        API '/translation/:uid' endpoint.

    MOCK_NONUPDATED_TRANSLATION
        Example of the returned json.dumps'd body of GETing to Unbabel
        API '/translation/:uid' endpoint, and the request hasn't updated
        yet.
    
    MOCK_LANGUAGE_PAIRS
        Example of the returned json.dumps'd body of GETing to Unbabel
        API '/language_pairs' endpoint.

    MOCK_UNBABELAPI_CONFIG
        Example of a complete configuration dict for making requests to
        Unbabel's API.

    MOCK_INCOMPLETE_UNBABELAPI_CONFIG
        Example of an incomplete configuration dict for making requests
        to Unbabel's API.
"""

from datetime import datetime


MOCK_TRANSLATIONS = (
    {
        'uid': 'uid0000001',
        'status': 'completed',
        'source_language': 'en',
        'target_language': 'es',
        'text': 'Sample text 1',
        'translated_text': 'El sample text 1',
        'text_length': 16,
        'date_created': datetime(2019, 12, 20, 15, 30, 45),
        'date_updated': datetime(2019, 12, 20, 15, 30, 45)
    },
    {
        'uid': 'uid0000002',
        'status': 'completed',
        'source_language': 'en',
        'target_language': 'es',
        'text': 'Sample text with a bit longer 2',
        'translated_text': 'El sample text dos',
        'text_length': 18,
        'date_created': datetime(2019, 12, 20, 15, 30, 45),
        'date_updated': datetime(2019, 12, 20, 15, 30, 45)
    },
    {
        'uid': 'uid0000003',
        'status': 'completed',
        'source_language': 'en',
        'target_language': 'es',
        'text': 'Sample text 3',
        'translated_text': 'El sample text tres',
        'text_length': 19,
        'date_created': datetime(2019, 12, 20, 15, 30, 45),
        'date_updated': datetime(2019, 12, 20, 15, 30, 45)
    },
    {
        'uid': 'uid0000004',
        'status': 'completed',
        'source_language': 'en',
        'target_language': 'es',
        'text': 'Sample text 4',
        'translated_text': 'El sample text quat',
        'text_length': 19,
        'date_created': datetime(2019, 12, 20, 15, 30, 45),
        'date_updated': datetime(2019, 12, 30, 15, 30, 45)
    },
    {
        'uid': 'uid0000005',
        'status': 'new',
        'source_language': 'en',
        'target_language': 'es',
        'text': 'Sample text 5',
        'translated_text': None,
        'text_length': 0,
        'date_created': datetime(2019, 12, 20, 15, 30, 45),
        'date_updated': datetime(2019, 12, 30, 15, 30, 45)
    },
)

MOCK_NEW_TRANSLATION = {
    'uid': 'uid0000new',
    'status': 'new',
    'source_language': 'en',
    'target_language': 'es',
    'text': 'New text please',
    'order_number': 1.0,
    'price': 8.0,
    'text_format': 'text'
}

MOCK_UPDATED_TRANSLATION = {
    'uid': 'uid0000005',
    'status': 'completed',
    'source_language': 'en',
    'target_language': 'es',
    'text': 'Sample text 5',
    'translatedText': 'Doraemon dejame jugar',
    'client': 'unbabel-fullstack-user',
    'price': 8.0,
    'text_format': 'text',
    'balance': 2682.0
}

MOCK_NONUPDATED_TRANSLATION = {
    'uid': 'uid0000005',
    'status': 'new',
    'source_language': 'en',
    'target_language': 'es',
    'text': 'Sample text 5',
    'translatedText': None,
    'client': 'unbabel-fullstack-user',
    'price': 8.0,
    'text_format': 'text',
    'balance': 2682.0
}

MOCK_LANGUAGE_PAIRS = {
    'objects': [
        {
            'lang_pair': {
                'source_language': {
                    'name': 'English',
                    'shortname': 'en'
                },
                'target_language': {
                    'name': 'Spanish',
                    'shortname': 'es'
                }
            }
        },
        {
            'lang_pair': {
                'source_language': {
                    'name': 'Portuguese',
                    'shortname': 'pt'
                },
                'target_language': {
                    'name': 'English',
                    'shortname': 'en'
                }
            }
        }
    ]
}

MOCK_UNBABELAPI_CONFIG = {
    'UNBABEL_USERNAME': 'unbabel-username',
    'UNBABEL_API_KEY': 'secret-unbabel-api-key'
}

MOCK_INCOMPLETE_UNBABELAPI_CONFIG = {
    'UNBABEL_USERNAME': 'unbabel-username'
}
