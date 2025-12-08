import os
import json
import requests
from config import db, test_env
from entities.reference import Reference


def get_references():
    """Get all references from the database."""
    return Reference.query.all()


def create_reference(reference):
    """Create a new reference in the database."""
    db.session.add(reference)
    db.session.commit()


def delete_reference(ref_id):
    """Delete a reference by ID."""
    reference = Reference.query.get(ref_id)
    if reference:
        db.session.delete(reference)
        db.session.commit()


def edit_reference(ref_id, reference):
    """Update an existing reference with new values."""
    existing_ref = Reference.query.get(ref_id)
    if existing_ref:
        existing_ref.reference_type = reference.reference_type
        existing_ref.cite_key = reference.cite_key
        existing_ref.title = reference.title
        existing_ref.author = reference.author
        existing_ref.year = reference.year

        # Update type-specific fields
        existing_ref.url = reference.url if hasattr(reference, "url") else None
        existing_ref.publisher = (
            reference.publisher if hasattr(reference, "publisher") else None
        )
        existing_ref.chapter = (
            reference.chapter if hasattr(reference, "chapter") else None
        )
        existing_ref.journal = (
            reference.journal if hasattr(reference, "journal") else None
        )
        existing_ref.volume = reference.volume if hasattr(reference, "volume") else None
        existing_ref.pages = reference.pages if hasattr(reference, "pages") else None
        existing_ref.booktitle = (
            reference.booktitle if hasattr(reference, "booktitle") else None
        )

        db.session.commit()


def get_reference(ref_id):
    """Get a single reference by ID."""
    return Reference.query.get(ref_id)


def get_reference_by_cite_key(cite_key):
    """Get a reference by its citation key."""
    return Reference.query.filter_by(cite_key=cite_key).first()


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
        return None
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

def search_references_by_query(query):
    """Search references by any field containing the query string."""
    if not query:
        return []

    search_pattern = f"%{query}%"

    return Reference.query.filter(
        (Reference.reference_type.ilike(search_pattern))
        | (Reference.cite_key.ilike(search_pattern))
        | (Reference.title.ilike(search_pattern))
        | (Reference.author.ilike(search_pattern))
        | (db.cast(Reference.year, db.String).ilike(search_pattern))
        | (Reference.url.ilike(search_pattern))
        | (Reference.publisher.ilike(search_pattern))
        | (Reference.chapter.ilike(search_pattern))
        | (Reference.journal.ilike(search_pattern))
        | (Reference.volume.ilike(search_pattern))
        | (Reference.pages.ilike(search_pattern))
        | (Reference.booktitle.ilike(search_pattern))
    ).all()


def search_references_advanced(filters):
    query = Reference.query

    # Apply title filter
    if filters.get("title"):
        query = query.filter(Reference.title.ilike(f"%{filters['title']}%"))

    # Apply author filter
    if filters.get("author"):
        query = query.filter(Reference.author.ilike(f"%{filters['author']}%"))

    # Apply year range filters
    if filters.get("year_from"):
        try:
            year_from = int(filters["year_from"])
            query = query.filter(Reference.year >= year_from)
        except ValueError:
            pass

    if filters.get("year_to"):
        try:
            year_to = int(filters["year_to"])
            query = query.filter(Reference.year <= year_to)
        except ValueError:
            pass

    # Apply reference type filter
    if filters.get("reference_type") and filters["reference_type"] != "all":
        query = query.filter(Reference.reference_type == filters["reference_type"])

    # Apply cite key filter
    if filters.get("cite_key"):
        query = query.filter(Reference.cite_key.ilike(f"%{filters['cite_key']}%"))

    # Apply journal filter (for articles)
    if filters.get("journal"):
        query = query.filter(Reference.journal.ilike(f"%{filters['journal']}%"))

    # Apply publisher filter (for books)
    if filters.get("publisher"):
        query = query.filter(Reference.publisher.ilike(f"%{filters['publisher']}%"))

    return query.all()
