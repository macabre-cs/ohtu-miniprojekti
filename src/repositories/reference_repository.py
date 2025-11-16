from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    result = db.session.execute(
        text('SELECT id, cite_key, title, year, publisher FROM references_table'))
    rows = result.mappings().all()
    return [Reference(row) for row in rows]


def create_reference(reference):
    sql = text("""INSERT INTO references_table (cite_key, title, year, publisher)
                  VALUES (:cite_key, :title, :year, :publisher)""")
    db.session.execute(sql, {"cite_key": reference.cite_key,
                             "title": reference.title,
                             "year": reference.year,
                             "publisher": reference.publisher})
    db.session.commit()
