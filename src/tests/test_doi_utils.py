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


def sample_book_message():
    return {
        "message": {
            "title": ["Test Book Title"],
            "author": [{"given": "Alice", "family": "Writer"}],
            "issued": {"date-parts": [[2018]]},
            "publisher": "Example Publisher",
            "chapter": "7",
            "type": "book",
        }
    }


def sample_article_with_article_number():
    return {
        "message": {
            "title": ["Article With Number"],
            "author": [{"given": "Sam", "family": "Example"}],
            "published-online": {"date-parts": [[2021]]},
            "container-title": ["Some Journal"],
            "article-number": "A123",
            "type": "journal-article",
        }
    }


def sample_authors_variants():
    return {
        "message": {
            "title": ["Author Variants"],
            "author": [
                {"given": "OnlyGiven"},
                {"family": "OnlyFamily"},
                {},
            ],
            "issued": {"date-parts": [[2019]]},
            "type": "journal-article",
        }
    }


def sample_html_entities_message():
    return {
        "message": {
            "title": ["Cats &amp; Dogs: A Study"],
            "author": [
                {"given": "Ann &amp; Co.", "family": "O'Neil"},
            ],
            "issued": {"date-parts": [[2022]]},
            "publisher": "Pets &amp; Friends Publishing",
            "container-title": ["Journal of Cats &amp; Dogs"],
            "page": "5&amp;-10",
            "type": "journal-article",
        }
    }


def test_parse_crossref_book_with_chapter():
    data = sample_book_message()
    parsed = parse_crossref(data, doi="10.9999/bookdoi")

    assert parsed["title"] == "Test Book Title"
    assert parsed["reference_type"] == "book"
    assert parsed["chapter"] == "7"


def test_parse_crossref_article_article_number_pages():
    data = sample_article_with_article_number()
    parsed = parse_crossref(data, doi="10.3000/num01")

    assert parsed["pages"] == "A123"
    assert parsed["reference_type"] == "article"


def test_parse_crossref_author_variants():
    data = sample_authors_variants()
    parsed = parse_crossref(data, doi="10.4000/var01")

    # should include the given-only and family-only entries without crashing
    assert "OnlyGiven" in parsed["authors"]
    assert "OnlyFamily" in parsed["authors"]


def test_parse_crossref_created_date_fallback():
    data = {"message": {"title": ["Created Date"], "created": {"date-parts": [[2015]]}}}
    parsed = parse_crossref(data, doi=None)
    assert parsed["year"] == "2015"


def test_parse_crossref_empty_input():
    assert parse_crossref(None) == {}
    assert parse_crossref({}) == {}


def test_cite_key_fallback_to_doi():
    data = {"message": {"title": ["No Authors"], "type": "journal-article"}}
    parsed = parse_crossref(data, doi="10.9999/testdoi")
    assert parsed["cite_key"] == "10.9999_testdoi"


def test_parse_crossref_unescapes_html_entities():
    data = sample_html_entities_message()
    parsed = parse_crossref(data, doi="10.5000/html01")

    assert parsed["title"] == "Cats & Dogs: A Study"
    assert parsed["authors"] == ["O'Neil, Ann & Co."]
    assert parsed["authors_formatted"] == "O'Neil, Ann & Co."
    assert parsed["publisher"] == "Pets & Friends Publishing"
    assert parsed["journal"] == "Journal of Cats & Dogs"
    assert parsed["pages"] == "5&-10"
