"""Helpers for parsing Crossref DOI lookup JSON into form fields.

This module provides `parse_crossref(metadata, doi=None)` which maps Crossref
`/works` responses to the form variables used by the templates. The
implementation is kept small and broken into private helper functions to make
unit testing and maintenance easier.
"""

from typing import Dict, Any, List, Tuple
import html


def _clean_text(value: Any) -> str:
    """Return a trimmed, HTML-unescaped string for text fields."""
    if value is None:
        return ""
    return html.unescape(str(value)).strip()


def _get_message(metadata: Any) -> Dict[str, Any]:
    """Return the Crossref message payload from the API response."""
    if not metadata or not isinstance(metadata, dict):
        return {}
    return metadata.get("message", {}) or {}


def _extract_title(msg: Dict[str, Any]) -> str:
    titles = msg.get("title") or []
    return _clean_text(titles[0]) if titles else ""


def _format_authors(msg: Dict[str, Any]) -> Tuple[List[str], str]:
    authors = []
    for a in msg.get("author", []):
        given = _clean_text(a.get("given"))
        family = _clean_text(a.get("family"))
        if family and given:
            authors.append(f"{family}, {given}")
        elif family:
            authors.append(family)
        elif given:
            authors.append(given)
    formatted = "; ".join(authors) if authors else ""
    return authors, formatted


def _extract_year(msg: Dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "issued"):
        dp = msg.get(key)
        if dp and isinstance(dp.get("date-parts"), list) and dp["date-parts"]:
            try:
                return str(int(dp["date-parts"][0][0]))
            except Exception:
                pass
    # fallback to `created`
    try:
        created = msg.get("created", {}).get("date-parts", [[None]])
        return str(int(created[0][0]))
    except Exception:
        return ""


def _determine_reference_type_and_booktitle(msg: Dict[str, Any], journal: str) -> Tuple[str, str]:
    typ = (msg.get("type") or "").lower()
    if "book" in typ:
        return "book", ""
    if "proceedings" in typ or (journal and "proceedings" in journal.lower()):
        return "inproceedings", journal
    return ("article", "") if journal else ("book", "")


def _suggest_cite_key(authors: List[str], year: str, doi: str | None) -> str:
    cite = ""
    if authors:
        first_family = authors[0].split(",", 1)[0]
        cite = f"{first_family}{year or ''}".replace(" ", "")
    if not cite and doi:
        cite = doi.replace("/", "_")
    return cite


def parse_crossref(metadata: Any, doi: str | None = None) -> Dict[str, Any]:
    """Map Crossref /works JSON to form fields used by templates.

    Returns a dict with keys matching template variables: title, authors (list),
    authors_formatted, year, publisher, journal, volume, pages, booktitle,
    chapter, reference_type, cite_key
    """
    if not metadata:
        return {}

    m = _get_message(metadata)
    out: Dict[str, Any] = {}

    out["title"] = _extract_title(m)

    authors, formatted = _format_authors(m)
    out["authors"] = authors
    out["authors_formatted"] = formatted

    out["year"] = _extract_year(m)
    out["publisher"] = _clean_text(m.get("publisher"))

    container = m.get("container-title") or []
    out["journal"] = _clean_text(container[0]) if container else ""

    out["volume"] = _clean_text(m.get("volume"))
    out["pages"] = _clean_text(m.get("page") or m.get("article-number"))

    out["chapter"] = _clean_text(m.get("chapter"))

    # type: ignore[arg-type]
    ref_type, booktitle = _determine_reference_type_and_booktitle(m, out["journal"])
    out["reference_type"] = ref_type
    out["booktitle"] = booktitle

    out["cite_key"] = _suggest_cite_key(authors, out["year"], doi)

    return out
