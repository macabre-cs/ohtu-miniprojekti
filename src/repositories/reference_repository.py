from config import db
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
        existing_ref.url = reference.url if hasattr(reference, 'url') else None
        existing_ref.publisher = reference.publisher if hasattr(reference, 'publisher') else None
        existing_ref.chapter = reference.chapter if hasattr(reference, 'chapter') else None
        existing_ref.journal = reference.journal if hasattr(reference, 'journal') else None
        existing_ref.volume = reference.volume if hasattr(reference, 'volume') else None
        existing_ref.pages = reference.pages if hasattr(reference, 'pages') else None
        existing_ref.booktitle = reference.booktitle if hasattr(reference, 'booktitle') else None

        db.session.commit()


def get_reference(ref_id):
    """Get a single reference by ID."""
    return Reference.query.get(ref_id)


def get_reference_by_cite_key(cite_key):
    """Get a reference by its citation key."""
    return Reference.query.filter_by(cite_key=cite_key).first()


def search_references_by_query(query):
    """Search references by any field containing the query string."""
    if not query:
        return []

    search_pattern = f"%{query}%"

    return Reference.query.filter(
        (Reference.reference_type.ilike(search_pattern)) |
        (Reference.cite_key.ilike(search_pattern)) |
        (Reference.title.ilike(search_pattern)) |
        (Reference.author.ilike(search_pattern)) |
        (db.cast(Reference.year, db.String).ilike(search_pattern)) |
        (Reference.url.ilike(search_pattern)) |
        (Reference.publisher.ilike(search_pattern)) |
        (Reference.chapter.ilike(search_pattern)) |
        (Reference.journal.ilike(search_pattern)) |
        (Reference.volume.ilike(search_pattern)) |
        (Reference.pages.ilike(search_pattern)) |
        (Reference.booktitle.ilike(search_pattern))
    ).all()
