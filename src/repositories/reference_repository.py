from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text(
            """SELECT id,
                      reference_type,
                      cite_key,
                      title,
                      author,
                      year,
                      publisher,
                      chapter,
                      journal,
                      volume,
                      pages,
                      booktitle,
                      created_at
            FROM references_table"""
        )
    )
    rows = result.mappings().all()
    return [Reference(row) for row in rows]


def create_reference(reference):
    if reference.reference_type == 'book':
        create_book_ref(reference)
    elif reference.reference_type == 'article':
        create_article_ref(reference)
    elif reference.reference_type == 'inproceedings':
        create_inproceedings_ref(reference)


def create_book_ref(reference):
    sql = text(
        """INSERT INTO references_table
           (reference_type, cite_key, title, author, year, publisher, chapter)
           VALUES (:reference_type,
                   :cite_key,
                   :title,
                   :author,
                   :year,
                   :publisher,
                   :chapter)"""
    )
    db.session.execute(
        sql,
        {
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "publisher": reference.publisher,
            "chapter": reference.chapter,
        },
    )
    db.session.commit()


def create_article_ref(reference):
    sql = text(
        """INSERT INTO references_table
           (reference_type, cite_key, title, author, year, journal, volume, pages)
           VALUES (:reference_type,
                   :cite_key,
                   :title,
                   :author,
                   :year,
                   :journal,
                   :volume,
                   :pages)"""
    )
    db.session.execute(
        sql,
        {
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "journal": reference.journal,
            "volume": reference.volume,
            "pages": reference.pages,
        },
    )
    db.session.commit()


def create_inproceedings_ref(reference):
    sql = text(
        """INSERT INTO references_table
           (reference_type, cite_key, title, author, year, booktitle)
           VALUES (:reference_type,
                   :cite_key,
                   :title,
                   :author,
                   :year,
                   :booktitle)"""
    )
    db.session.execute(sql, {"reference_type": reference.reference_type,
                             "cite_key": reference.cite_key,
                             "title": reference.title,
                             "author": reference.author,
                             "year": reference.year,
                             "booktitle": reference.booktitle})
    db.session.commit()


def delete_reference(ref_id):
    sql = text("""DELETE FROM references_table WHERE id = :id""")
    db.session.execute(sql, {"id": ref_id})
    db.session.commit()


def edit_reference(ref_id, reference):
    sql = text(
        """UPDATE references_table
                  SET cite_key = :cite_key,
                      title = :title,
                      author = :author,
                      year = :year,
                      publisher = :publisher
                  WHERE id = :id"""
    )
    db.session.execute(
        sql,
        {
            "id": ref_id,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "publisher": reference.publisher,
        },
    )
    db.session.commit()


def get_reference(ref_id):
    sql = text(
        """SELECT id, reference_type, cite_key, author, title, year, publisher
            FROM references_table WHERE id = :id"""
    )
    result = db.session.execute(sql, {"id": ref_id})
    row = result.mappings().first()
    if not row:
        return None

    return Reference(row)


def get_reference_by_cite_key(cite_key):
    sql = text(
        """SELECT id, cite_key, title, author, year, publisher
            FROM references_table WHERE cite_key = :cite_key"""
    )
    result = db.session.execute(sql, {"cite_key": cite_key})
    row = result.mappings().first()
    if not row:
        return None

    return Reference(row)
