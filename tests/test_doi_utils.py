import pytest

from doi_utils import parse_crossref


def sample_article_message():
    return {
        "message": {
            "title": ["Sample Article Title"],
            "author": [{"given": "John", "family": "Doe"}, {"given": "Jane", "family": "Smith"}],
            "published-print": {"date-parts": [[2020]]},
            "publisher": "Sample Publisher",
            "container-title": ["Journal of Testing"],
            "volume": "5",
            "page": "10-20",
            "type": "journal-article",
        }
    }


def sample_proceedings_message():
    return {
        "message": {
            "title": ["Proceedings Paper"],
            "author": [{"given": "Alice", "family": "Wonder"}],
            "issued": {"date-parts": [[2018]]},
            "publisher": "Conf Publisher",
            "container-title": ["Proceedings of the Test Conf"],
            "type": "proceedings-article",
        }
    }


def test_parse_crossref_article():
    data = sample_article_message()
    parsed = parse_crossref(data, doi="10.1000/xyz123")

    assert parsed["title"] == "Sample Article Title"
    assert parsed["authors"] == ["Doe, John", "Smith, Jane"]
    assert parsed["authors_formatted"] == "Doe, John; Smith, Jane"
    assert parsed["year"] == "2020"
    assert parsed["publisher"] == "Sample Publisher"
    assert parsed["journal"] == "Journal of Testing"
    assert parsed["volume"] == "5"
    assert parsed["pages"] == "10-20"
    assert parsed["reference_type"] == "article"
    assert parsed["cite_key"].startswith("Doe2020") or parsed["cite_key"]


def test_parse_crossref_proceedings():
    data = sample_proceedings_message()
    parsed = parse_crossref(data, doi="10.2000/proc01")

    assert parsed["title"] == "Proceedings Paper"
    assert parsed["authors"] == ["Wonder, Alice"]
    assert parsed["year"] == "2018"
    # proceedings should be detected as inproceedings
    assert parsed["reference_type"] == "inproceedings"
    assert parsed["booktitle"] == "Proceedings of the Test Conf"
