from repositories.reference_repository import get_reference_by_cite_key

class UserInputError(Exception):
    pass


def validate_reference(reference_dict):
    def value(key):
        return (reference_dict.get(key) or "").strip()

    if not value("reference_type"):
        raise ValueError("Reference type is required")
    if not value("cite_key"):
        raise ValueError("Cite key is required")
    if not value("title"):
        raise ValueError("Title is required")
    if not value("author"):
        raise ValueError("Author(s) is/are required")

    year_raw = reference_dict.get("year")
    if year_raw is None or not str(year_raw).strip():
        raise ValueError("Year is required")
    try:
        int(year_raw)
    except (ValueError, TypeError) as exc:
        raise ValueError("Year must be a valid number") from exc

def validate_cite_key(cite_key, exclude_id=None):
    reference = get_reference_by_cite_key(cite_key)
    if reference and (exclude_id is None or str(reference.id) != str(exclude_id)):
        raise ValueError("Cite key already exists")
