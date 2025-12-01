import requests
import json
import os
from config import db, test_env
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
    if reference.reference_type == 'book':
        edit_book_ref(ref_id, reference)
    elif reference.reference_type == 'article':
        edit_article_ref(ref_id, reference)
    elif reference.reference_type == 'inproceedings':
        edit_inproceedings_ref(ref_id, reference)

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
            "chapter": reference.chapter
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


def get_reference(ref_id):
    sql = text(
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


def get_reference_by_doi(doi):
    # Test-mode stub: return fixture for known test DOIs to avoid external calls
    # We expect fixtures named `crossref_test_<key>.json` where <key> is the
    # final path segment of the DOI (e.g. 10.9999/testdoi -> crossref_test_testdoi.json)
    if test_env and doi:
        try:
            key = doi.strip().split("/")[-1]
            fixture_name = f"crossref_test_{key}.json"
            # Prefer fixtures in project root `tests/fixtures`, but also support
            # `src/tests/fixtures` where unit tests may live.
            candidate_paths = [
                os.path.join(os.getcwd(), "tests", "fixtures", fixture_name),
                os.path.join(os.getcwd(), "src", "tests", "fixtures", fixture_name),
            ]
            for fixture_path in candidate_paths:
                if os.path.exists(fixture_path):
                    with open(fixture_path, "r", encoding="utf-8") as fh:
                        return json.load(fh)
        except Exception:
            pass

    # Normal behavior: call Crossref API. Ensure DOI is URL-encoded and normalized.
    # Accept inputs like 'doi:10.1234/abcd' or full DOI URLs.
    d = doi.strip()
    if d.lower().startswith("doi:"):
        d = d[4:]
    if d.startswith("http://") or d.startswith("https://"):
        # extract path part
        d = d.split("/", 3)[-1]

    # Use the Crossref works endpoint
    url = f"https://api.crossref.org/works/{requests.utils.requote_uri(d)}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
