"""
This module sits between the application and the data layer, abstracting
the connection to the database with SQLAlchemy, and creates the models
for the data stored in the database.

db : SQLAlchemy
    SQLAlchemy instantiation. This object represents the connection to the
    database. It is created without an explicit app binding so that it can
    be bound later in the Flask application factory. It knows about any
    class that extends SQLAlchemy.Model and treats it as a model for
    databse queries.

class Translation
    Extends SQLAlchemy.Model. Model abstraction on top of the
    'translations' table in the database.
"""


from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy()


class Translation(db.Model):
    """
    A Translation is a record for a translation request by the user,
    stored with default values when the Unbabel API returns the 201
    Created response.

    Each translation that is not in a completed state is subject to
    update through querying the Unbabel API with its UID.
    Completed translations stay untouched, and their translations
    stored for easy access without further calls to the Unbabel
    API.

    Attributes:
        __tablename__
            SQLAlchemy attribute. Sets the name of the table in the
            database.
        uid
            Unique ID assigned by the Unbabel API.
        status
            Status of the translation.
        source_lang
            Code for the language of the text to be translated.
        target_lang
            Code for the language of the translated text.
        test
            Text to be translated.
        translated_text
            None if the text hasn't been translated yet. Translated
            text returned by Unbabel's API, otherwise.
        text_length
            Length of the translated text, computed and stored as soon
            as the translated text is received. Storing this value
            makes it easier to order the results when needed.
        date_created
            Timestamp of the creation of the translation request.
        date_updated
            Timestamp of the last update done to this translation
            request.

    Class Methods:
        get_all(cls)
            Return all the translations in the database.

    Instance Methods:
        dictify(self)
            Turn a Translation instance into a Python dictionary
            for easy serialization.
    """

    __tablename__ = 'translations'

    uid = sa.Column(sa.String(10), primary_key=True)
    status = sa.Column(sa.String(), nullable=False)
    source_lang = sa.Column(sa.String(), nullable=False)
    target_lang = sa.Column(sa.String(), nullable=False)

    text = sa.Column(sa.Text(), nullable=False)
    translated_text = sa.Column(sa.Text(), default=None)
    text_length = sa.Column(sa.Integer(), default=0)

    date_created = sa.Column(sa.DateTime(
        timezone=True), default=datetime.utcnow)
    date_updated = sa.Column(sa.DateTime(timezone=True),
                             default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_all(cls):
        """
        Return all translations, ordered by length of translated
        text (desc), and then date of last update (desc).
        """
        return cls.query.order_by(
            sa.desc(cls.text_length)
        ).order_by(
            sa.desc(cls.date_updated)
        ).all()

    def dictify(self):
        """
        Transform a table record into a dictionary of its attributes
        fit for serialization.
        """
        return {
            'uid': self.uid,
            'status': self.status,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'text': self.text,
            'translated_text': self.translated_text,
            'text_length': self.text_length,
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'date_updated': self.date_updated.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __repr__(self):
        """
        Return the representation of the instance.
        """
        return '<Translation [{source_lang} -> {target_lang}] "{text:.16}">'.format(
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            text=self.text
        )