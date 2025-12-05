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
    # In test mode prefer local fixtures to avoid external HTTP calls.
    if test_env and doi:
        fixture = _load_fixture_for_doi(doi)
        if fixture:
            return fixture

    # Normalize DOI input and call Crossref API.
    d = _normalize_doi(doi)
    if not d:
        return None

    url = f"https://api.crossref.org/works/{requests.utils.requote_uri(d)}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        # Keep behavior simple for callers: return None on any error.
        return None

    try:
        return response.json()
    except ValueError:
        return None


def _load_fixture_for_doi(doi: str):
    """Return a fixture dict for a test DOI or None.

    Fixtures are searched in `tests/fixtures` and `src/tests/fixtures`.
    The fixture filename is `crossref_test_<last_segment>.json`.
    """
    try:
        key = doi.strip().split("/")[-1]
        fixture_name = f"crossref_test_{key}.json"
        candidate_paths = [
            os.path.join(os.getcwd(), "tests", "fixtures", fixture_name),
            os.path.join(os.getcwd(), "src", "tests", "fixtures", fixture_name),
        ]
        for fixture_path in candidate_paths:
            if os.path.exists(fixture_path):
                with open(fixture_path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
    except Exception:
        return None


def _normalize_doi(doi: str | None) -> str | None:
    """Normalize user-provided DOI strings to the raw identifier used by Crossref.

    Accepts values like 'doi:10.1234/abcd', full URLs, or plain DOIs.
    Returns None for empty inputs.
    """
    if not doi:
        return None
    d = doi.strip()
    if not d:
        return None
    if d.lower().startswith("doi:"):
        d = d[4:]
    if d.startswith("http://") or d.startswith("https://"):
        # extract the path portion after the domain
        parts = d.split("/", 3)
        if len(parts) >= 4:
            d = parts[3]
        else:
            # fallback: use last segment
            d = d.split("/")[-1]
    return d
