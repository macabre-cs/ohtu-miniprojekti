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
                      url,
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
    if reference.reference_type == "book":
        create_book_ref(reference)
    elif reference.reference_type == "article":
        create_article_ref(reference)
    elif reference.reference_type == "inproceedings":
        create_inproceedings_ref(reference)
    elif reference.reference_type == "misc":
        create_misc_ref(reference)


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
    db.session.execute(
        sql,
        {
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "booktitle": reference.booktitle,
        },
    )
    db.session.commit()


def create_misc_ref(reference):
    sql = text(
        """INSERT INTO references_table
           (reference_type, cite_key, title, author, year, url)
           VALUES (:reference_type,
                   :cite_key,
                   :title,
                   :author,
                   :year,
                   :url)"""
    )
    db.session.execute(
        sql,
        {
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "url": reference.url,
        },
    )
    db.session.commit()


def delete_reference(ref_id):
    sql = text("""DELETE FROM references_table WHERE id = :id""")
    db.session.execute(sql, {"id": ref_id})
    db.session.commit()


def edit_reference(ref_id, reference):
    if reference.reference_type == "book":
        edit_book_ref(ref_id, reference)
    elif reference.reference_type == "article":
        edit_article_ref(ref_id, reference)
    elif reference.reference_type == "inproceedings":
        edit_inproceedings_ref(ref_id, reference)
    elif reference.reference_type == "misc":
        edit_misc_ref(ref_id, reference)


def edit_book_ref(ref_id, reference):
    sql = text(
        """UPDATE references_table
                  SET reference_type = :reference_type,
                      cite_key = :cite_key,
                      title = :title,
                      author = :author,
                      year = :year,
                      publisher = :publisher,
                      chapter = :chapter
                  WHERE id = :id"""
    )
    db.session.execute(
        sql,
        {
            "id": ref_id,
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


def edit_article_ref(ref_id, reference):
    sql = text(
        """UPDATE references_table
           SET reference_type = :reference_type,
               cite_key = :cite_key,
               title = :title,
               author = :author,
               year = :year,
               journal = :journal,
               volume = :volume,
               pages = :pages
           WHERE id = :id"""
    )
    db.session.execute(
        sql,
        {
            "id": ref_id,
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


def edit_inproceedings_ref(ref_id, reference):
    sql = text(
        """UPDATE references_table
           SET reference_type = :reference_type,
               cite_key = :cite_key,
               title = :title,
               author = :author,
               year = :year,
               booktitle = :booktitle
           WHERE id = :id"""
    )
    db.session.execute(
        sql,
        {
            "id": ref_id,
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "booktitle": reference.booktitle,
        },
    )
    db.session.commit()


def edit_misc_ref(ref_id, reference):
    sql = text(
        """UPDATE references_table
           SET reference_type = :reference_type,
               cite_key = :cite_key,
               title = :title,
               author = :author,
               year = :year,
               url = :url
           WHERE id = :id"""
    )
    db.session.execute(
        sql,
        {
            "id": ref_id,
            "reference_type": reference.reference_type,
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "url": reference.url,
        },
    )
    db.session.commit()


def get_reference(ref_id):
    sql = text(
        """SELECT id, 
                  reference_type,
                  cite_key, 
                  title,
                  author, 
                  year,
                  url,
                  publisher, 
                  chapter, 
                  journal, 
                  volume, 
                  pages, 
                  booktitle
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


def search_references_by_query(query):
    sql = text(
        """SELECT id,
                reference_type,
                cite_key,
                title,
                author,
                year,
                url,
                publisher,
                chapter,
                journal,
                volume,
                pages,
                booktitle
            FROM references_table WHERE
                reference_type ILIKE :query OR
                cite_key ILIKE :query OR
                title ILIKE :query OR
                author ILIKE :query OR
                CAST(year AS TEXT) ILIKE :query OR
                url ILIKE :query OR
                publisher ILIKE :query OR
                chapter ILIKE :query OR
                journal ILIKE :query OR
                CAST(volume AS TEXT) ILIKE :query OR
                CAST(pages AS TEXT) ILIKE :query OR
                booktitle ILIKE :query
        """
    )

    like = "%" + query + "%"
    result = db.session.execute(sql, {"query": like})
    rows = result.mappings().all()

    if not rows:
        return []

    return [Reference(row) for row in rows]
