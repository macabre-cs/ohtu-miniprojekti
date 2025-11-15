from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text('SELECT id, cite_key, title, year, publisher FROM references_table'))
    rows = result.fetchall()
    return [Reference(r[0], r[1], r[2], r[3], r[4]) for r in rows]


def create_reference(reference):
    sql = text("""INSERT INTO references_table (cite_key, title, year, publisher)
                  VALUES (:cite_key, :title, :year, :publisher)""")
    db.session.execute(sql, {"cite_key": reference.cite_key,
                             "title": reference.title,
                             "year": reference.year,
                             "publisher": reference.publisher})
    db.session.commit()
