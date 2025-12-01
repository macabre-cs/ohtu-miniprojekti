"""Helpers for parsing Crossref DOI lookup JSON into form fields.

This module contains a single function `parse_crossref(metadata, doi=None)` that
maps Crossref `/works` responses to the form variables expected by
`new_reference.html` and the `new_*` partial templates.
"""

def parse_crossref(metadata, doi=None):
    """Map Crossref /works JSON to form fields used by templates.

    Returns a dict with keys matching template variables: title, authors (list),
    authors_formatted, year, publisher, journal, volume, pages, booktitle,
    reference_type, cite_key
    """
    if not metadata:
        return {}

    m = metadata.get("message", {}) if isinstance(metadata, dict) else {}
    out = {}

    # title
    titles = m.get("title") or []
    out["title"] = titles[0] if titles else ""

    # authors
    authors = []
    for a in m.get("author", []):
        given = (a.get("given") or "").strip()
        family = (a.get("family") or "").strip()
        if family and given:
            authors.append(f"{family}, {given}")
        elif family:
            authors.append(family)
        elif given:
            authors.append(given)
    out["authors"] = authors
    out["authors_formatted"] = "; ".join(authors) if authors else ""

    # year: check published-print, published-online, issued
    def extract_year(msg):
        for key in ("published-print", "published-online", "issued"):
            dp = msg.get(key)
            if dp and isinstance(dp.get("date-parts"), list) and dp["date-parts"]:
                try:
                    return int(dp["date-parts"][0][0])
                except Exception:
                    pass
        # fallback
        try:
            return int(msg.get("created", {}).get("date-parts", [[None]])[0][0])
        except Exception:
            return None

    year = extract_year(m)
    out["year"] = str(year) if year else ""

    out["publisher"] = m.get("publisher") or ""

    container = m.get("container-title") or []
    out["journal"] = container[0] if container else ""

    out["volume"] = m.get("volume") or ""
    out["pages"] = m.get("page") or m.get("article-number") or ""

    # chapter (if present for book entries)
    out["chapter"] = m.get("chapter") or ""

    out["booktitle"] = ""
    typ = (m.get("type") or "").lower()
    # heuristics for reference_type
    if "book" in typ:
        out["reference_type"] = "book"
    elif "proceedings" in typ or "proceedings" in (out["journal"].lower() if out["journal"]
                                                                          else ""):
        out["reference_type"] = "inproceedings"
        out["booktitle"] = out["journal"]
    else:
        # prefer article when we have a container title
        out["reference_type"] = "article" if out["journal"] else "book"

    # simple cite_key suggestion: first author's family + year, or DOI sanitized
    cite = ""
    if authors:
        first_family = authors[0].split(",", 1)[0]
        cite = f"{first_family}{year or ''}".replace(" ", "")
    if not cite and doi:
        cite = doi.replace("/", "_")
    out["cite_key"] = cite
    return out
