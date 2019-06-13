import pytest

from cervantes.models import Translation


class TestTranslation():
    def test_get_all(self, db):
        """Check if the records are produced in the correct order."""

        translation_ids = [t.uid for t in Translation.get_all()]

        expected_order = ['uid0000004', 'uid0000003',
                          'uid0000002', 'uid0000001', 'uid0000005', ]

        assert translation_ids == expected_order

    def test_get_all_pending(self, db):
        """Check if the records are filtered correctly."""

        translation_ids = [t.uid for t in Translation.get_all_pending()]

        expected_ids = ['uid0000005', ]

        assert translation_ids == expected_ids

    def test_representation(self, db):
        """Test the __repr__ format of the Translation records"""

        translations = Translation.query.all()

        assert translations[0].__repr__(
        ) == '<Translation (completed) [en -> es] "Sample text 1">'
        assert translations[1].__repr__(
        ) == '<Translation (completed) [en -> es] "Sample text with">'
        assert translations[4].__repr__(
        ) == '<Translation (new) [en -> es] "Sample text 5">'

    def test_dictify(self, db):
        """Test the serialization method of the Translation records"""

        translations = Translation.query.all()

        completed_translation = {
            'uid': 'uid0000001',
            'status': 'completed',
            'source_language': 'en',
            'target_language': 'es',
            'text': 'Sample text 1',
            'translated_text': 'El sample text 1',
            'text_length': 16,
            'date_created': '2019-12-20 15:30:45',
            'date_updated': '2019-12-20 15:30:45',
        }

        new_translation = {
            'uid': 'uid0000005',
            'status': 'new',
            'source_language': 'en',
            'target_language': 'es',
            'text': 'Sample text 5',
            'translated_text': None,
            'text_length': 0,
            'date_created': '2019-12-20 15:30:45',
            'date_updated': '2019-12-30 15:30:45',
        }

        assert translations[0].dictify() == completed_translation
        assert translations[4].dictify() == new_translation
