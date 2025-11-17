class UserInputError(Exception):
    pass


def validate_reference(cite_key, title, author, year, publisher):
    if not cite_key or not cite_key.strip():
        raise ValueError("Cite key is required")
    if not title or not title.strip():
        raise ValueError("Title is required")
    if not author or not author.strip():
        raise ValueError("Author(s) is/are required")
    if not year or not str(year).strip():
        raise ValueError("Year is required")
    try:
        int(year)
    except (ValueError, TypeError) as exc:
        raise ValueError("Year must be a valid number") from exc
    if not publisher or not publisher.strip():
        raise ValueError("Publisher is required")
