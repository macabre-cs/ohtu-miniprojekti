from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text('SELECT * FROM references_table'))
    rows = result.mappings().all()
    return [Reference(row) for row in rows]


def create_reference(reference):
    if reference.reference_type == 'book':
        return create_book_ref(reference)
    elif reference.reference_type == 'article':
        return create_article_ref(reference)
    elif reference.reference_type == 'inproceedings':
        return create_inproceedings_ref(reference)

def create_book_ref(reference):
    sql = text("""INSERT INTO references_table (reference_type, cite_key, title, author, year, publisher, chapter)
                  VALUES (:reference_type, :cite_key, :title, :author, :year, :publisher, :chapter)""")
    db.session.execute(sql, {"reference_type": reference.reference_type,
                             "cite_key": reference.cite_key,
                             "title": reference.title,
                             "author": reference.author,
                             "year": reference.year,
                             "publisher": reference.publisher,
                             "chapter": reference.chapter})
    db.session.commit()

def create_article_ref(reference):
    sql = text("""INSERT INTO references_table (reference_type, cite_key, title, author, year, journal, volume, pages)
                  VALUES (:reference_type, :cite_key, :title, :author, :year, :journal, :volume, :pages)""")
    db.session.execute(sql, {"reference_type": reference.reference_type,
                             "cite_key": reference.cite_key,
                             "title": reference.title,
                             "author": reference.author,
                             "year": reference.year,
                             "journal": reference.journal,
                             "volume": reference.volume,
                             "pages": reference.pages})
    db.session.commit()

def create_inproceedings_ref(reference):
    sql = text("""INSERT INTO references_table (reference_type, cite_key, title, author, year, booktitle)
                  VALUES (:reference_type, :cite_key, :title, :author, :year, :booktitle)""")
    db.session.execute(sql, {"reference_type": reference.reference_type,
                             "cite_key": reference.cite_key,
                             "title": reference.title,
                             "author": reference.author,
                             "year": reference.year,
                             "booktitle": reference.booktitle})
    db.session.commit()