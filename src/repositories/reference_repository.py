from sqlalchemy import text
from config import db

from entities.reference import Reference

def get_references():
    result = db.session.execute(text('SELECT id, content FROM references_table'))
    rows = result.fetchall()
    return [Reference(r[0], r[1]) for r in rows]

def create_reference(content):
    sql = text('INSERT INTO references_table (content) VALUES (:content)')
    db.session.execute(sql, { "content": content })
    db.session.commit()
