from unittest.mock import MagicMock, patch
from repositories.reference_repository import (
    get_references,
    create_reference,
    get_reference,
    delete_reference,
    edit_reference,
    search_references_by_query
    )
from entities.reference import Reference

@patch("repositories.reference_repository.Reference")
def test_get_references(mock_reference_class):
    # Mock the query.all() to return a list of references
    mock_ref1 = MagicMock()
    mock_ref1.cite_key = "key1"
    mock_ref1.title = "Title 1"

    mock_ref2 = MagicMock()
    mock_ref2.cite_key = "key2"
    mock_ref2.title = "Title 2"

    mock_reference_class.query.all.return_value = [mock_ref1, mock_ref2]

    references = get_references()

    # test for correct amount of results
    assert len(references) == 2
    # test a specific field
    assert references[0].title == "Title 1"
    # check that the query was called
    mock_reference_class.query.all.assert_called_once()


@patch("repositories.reference_repository.db")
def test_create_book_reference(mock_db):
    reference_dict_test = {
        "reference_type": "book",
        "cite_key": "key3",
        "title": "Title 3",
        "author": "Author 3",
        "year": 2022,
        "publisher": "Publisher C",
        "chapter": "Chapter 1"
    }

    reference = Reference(reference_dict_test)

    assert reference.reference_type == "book"
    assert reference.cite_key == "key3"
    assert reference.title == "Title 3"
    assert reference.author == "Author 3"
    assert reference.year == 2022
    assert reference.publisher == "Publisher C"
    assert reference.chapter == "Chapter 1"

    create_reference(reference)

    # check that add gets called with the reference
    mock_db.session.add.assert_called_once_with(reference)

    # check that the function commits
    mock_db.session.commit.assert_called_once()


@patch("repositories.reference_repository.db")
def test_create_article_reference(mock_db):
    reference_dict_test = {
        "reference_type": "article",
        "cite_key": "key4",
        "title": "Article Title",
        "author": "Article Author",
        "year": 2023,
        "journal": "Journal X",
        "volume": "42",
        "pages": "10-20"
    }

    reference = Reference(reference_dict_test)

    assert reference.reference_type == "article"
    assert reference.cite_key == "key4"
    assert reference.title == "Article Title"
    assert reference.author == "Article Author"
    assert reference.year == 2023
    assert reference.journal == "Journal X"
    assert reference.volume == "42"
    assert reference.pages == "10-20"

    create_reference(reference)

    # check that add gets called with the reference
    mock_db.session.add.assert_called_once_with(reference)

    # check that the function commits
    mock_db.session.commit.assert_called_once()


@patch("repositories.reference_repository.db")
def test_create_inproceedings_reference(mock_db):
    reference_dict_test = {
        "reference_type": "inproceedings",
        "cite_key": "key5",
        "title": "Inproc Title",
        "author": "Inproc Author",
        "year": 2024,
        "booktitle": "Proceedings Y"
    }

    reference = Reference(reference_dict_test)

    assert reference.reference_type == "inproceedings"
    assert reference.cite_key == "key5"
    assert reference.title == "Inproc Title"
    assert reference.author == "Inproc Author"
    assert reference.year == 2024
    assert reference.booktitle == "Proceedings Y"

    create_reference(reference)

    # check that add gets called with the reference
    mock_db.session.add.assert_called_once_with(reference)

    # check that the function commits
    mock_db.session.commit.assert_called_once()

@patch("repositories.reference_repository.db")
def test_misc_reference(mock_db):
    reference_dict_test = {
        "reference_type": "misc",
        "cite_key": "key6",
        "title": "Scrum (project management)",
        "author": "Wikipedia",
        "year": 2025,
        "url": "https://en.wikipedia.org/wiki/Scrum_(project_management)"
    }

    reference = Reference(reference_dict_test)

    assert reference.reference_type == "misc"
    assert reference.cite_key == "key6"
    assert reference.title == "Scrum (project management)"
    assert reference.author == "Wikipedia"
    assert reference.year == 2025
    assert reference.url == "https://en.wikipedia.org/wiki/Scrum_(project_management)"

    create_reference(reference)

    # check that add gets called with the reference
    mock_db.session.add.assert_called_once_with(reference)

    # check that the function commits
    mock_db.session.commit.assert_called_once()

@patch("repositories.reference_repository.Reference")
def test_get_reference_found(mock_reference_class):
    # Create a mock reference
    mock_ref = MagicMock()
    mock_ref.id = 1
    mock_ref.cite_key = "key1"
    mock_ref.title = "Title 1"
    mock_ref.author = "Author 1"
    mock_ref.year = 2020

    mock_reference_class.query.get.return_value = mock_ref

    ref = get_reference(1)

    assert ref.title == "Title 1"
    # ensure query.get was called with the correct id
    mock_reference_class.query.get.assert_called_once_with(1)


@patch("repositories.reference_repository.Reference")
def test_get_reference_not_found(mock_reference_class):
    mock_reference_class.query.get.return_value = None

    ref = get_reference(999)
    assert ref is None
    mock_reference_class.query.get.assert_called_once_with(999)


@patch("repositories.reference_repository.db")
@patch("repositories.reference_repository.Reference")
def test_delete_reference(mock_reference_class, mock_db):
    # Create a mock reference to be deleted
    mock_ref = MagicMock()
    mock_reference_class.query.get.return_value = mock_ref

    delete_reference(5)

    # Ensure query.get was called with correct id
    mock_reference_class.query.get.assert_called_once_with(5)
    # Ensure delete was called with the reference
    mock_db.session.delete.assert_called_once_with(mock_ref)
    # Ensure commit was called
    mock_db.session.commit.assert_called_once()


@patch("repositories.reference_repository.db")
@patch("repositories.reference_repository.Reference")
def test_edit_reference(mock_reference_class, mock_db):
    # Create a mock existing reference
    mock_existing_ref = MagicMock()
    mock_existing_ref.id = 3
    mock_reference_class.query.get.return_value = mock_existing_ref

    reference_dict_test = {
        "reference_type": "book",
        "cite_key": "edited_key",
        "title": "Edited Title",
        "author": "Edited Author",
        "year": 2030,
        "publisher": "Edited Publisher",
        "chapter": "Chapter 5"
    }

    reference = Reference(reference_dict_test)

    edit_reference(3, reference)

    # Ensure query.get was called
    mock_reference_class.query.get.assert_called_once_with(3)

    # Check that the existing reference was updated
    assert mock_existing_ref.cite_key == "edited_key"
    assert mock_existing_ref.title == "Edited Title"
    assert mock_existing_ref.author == "Edited Author"
    assert mock_existing_ref.year == 2030
    assert mock_existing_ref.publisher == "Edited Publisher"

    # ensure commit was called
    mock_db.session.commit.assert_called_once()


@patch("repositories.reference_repository.Reference")
def test_search_reference_by_query(mock_reference_class):
    # Mock query filter and all() to return search results
    mock_ref1 = MagicMock()
    mock_ref1.title = "Test Result 1"

    mock_ref2 = MagicMock()
    mock_ref2.title = "Test Result 2"

    # Mock the query chain
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = [mock_ref1, mock_ref2]
    mock_reference_class.query = mock_query

    results = search_references_by_query("test query")

    # Verify results
    assert len(results) == 2
    assert results[0].title == "Test Result 1"

    mock_query.filter.assert_called_once()
