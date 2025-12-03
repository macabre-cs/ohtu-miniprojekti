# pylint: disable=too-many-instance-attributes

from datetime import datetime
from config import db

class Reference(db.Model):
    __tablename__ = 'references_table'
    
    id = db.Column(db.Integer, primary_key=True)
    reference_type = db.Column(db.String, nullable=False)
    cite_key = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String)
    publisher = db.Column(db.String)
    chapter = db.Column(db.String)
    journal = db.Column(db.String)
    volume = db.Column(db.String)
    pages = db.Column(db.String)
    booktitle = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, reference_dict=None, **kwargs):
        """
        Initialize Reference from dictionary or keyword arguments.
        Supports both dict-based (legacy) and ORM-based initialization.
        """
        if reference_dict is not None:
            # Dictionary-based initialization (for backward compatibility)
            super().__init__()
            self.reference_type = reference_dict.get('reference_type')
            self.cite_key = reference_dict.get('cite_key')
            self.title = reference_dict.get('title')
            self.author = reference_dict.get('authors_formatted') or reference_dict.get('author')
            self.year = reference_dict.get('year')
            self.url = reference_dict.get('url')
            self.publisher = reference_dict.get('publisher')
            self.chapter = reference_dict.get('chapter')
            self.journal = reference_dict.get('journal')
            self.volume = reference_dict.get('volume')
            self.pages = reference_dict.get('pages')
            self.booktitle = reference_dict.get('booktitle')
            
            # Handle id separately (for existing records)
            if 'id' in reference_dict:
                self.id = reference_dict.get('id')
        else:
            # Keyword argument initialization (ORM style)
            super().__init__(**kwargs)

    def __str__(self):
        cite = self.cite_key or ""
        title = self.title or ""
        year = self.year or ""
        author = self.author or ""

        return f"{cite}: {title} ({year}), {author}"

    def __iter__(self):
        result = {
            'id': self.id,
            'reference_type': self.reference_type,
            'cite_key': self.cite_key,
            'title': self.title,
            'author': self.author,
            'year': self.year
        }

        if self.reference_type == 'book':
            result['publisher'] = self.publisher
            result['chapter'] = self.chapter
        elif self.reference_type == 'article':
            result['journal'] = self.journal
            result['volume'] = self.volume
            result['pages'] = self.pages
        elif self.reference_type == 'inproceedings':
            result['booktitle'] = self.booktitle
        elif self.reference_type == 'misc':
            result['url'] = self.url

        return iter(result.items())
