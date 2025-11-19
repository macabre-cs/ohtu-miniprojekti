from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text('SELECT id, cite_key, title, author, year, publisher FROM references_table'))
    rows = result.mappings().all()
    return [Reference(row) for row in rows]


def create_reference(reference):
    sql = text("""INSERT INTO references_table (cite_key, title, author, year, publisher)
                  VALUES (:cite_key, :title, :author, :year, :publisher)""")
    db.session.execute(sql, {"cite_key": reference.cite_key,
                             "title": reference.title,
                             "author": reference.author,
                             "year": reference.year,
                             "publisher": reference.publisher})
    db.session.commit()


def delete_reference(cite_key):
    sql = text("""DELETE FROM references_table WHERE cite_key = :cite_key""")
    db.session.execute(sql, {"cite_key": cite_key})
    db.session.commit()


def get_reference(cite_key):
    sql = text("""SELECT id, cite_key, author, title, year, publisher
            FROM references_table WHERE cite_key = :cite_key""")
    result = db.session.execute(sql, {"cite_key": cite_key})
    row = result.mappings().first()
    if not row:
        return None

    return Reference(row)
