from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from util import UserInputError

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text(
            "SELECT id, cite_key, title, author, year, publisher FROM references_table"
        )
    )
    rows = result.mappings().all()
    return [Reference(row) for row in rows]


def create_reference(reference):
    sql = text(
        """INSERT INTO references_table (cite_key, title, author, year, publisher)
                  VALUES (:cite_key, :title, :author, :year, :publisher)"""
    )
    db.session.execute(
        sql,
        {
            "cite_key": reference.cite_key,
            "title": reference.title,
            "author": reference.author,
            "year": reference.year,
            "publisher": reference.publisher,
        },
    )
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
        """SELECT id, cite_key, author, title, year, publisher
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
