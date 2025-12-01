from unittest.mock import MagicMock, patch
from repositories.reference_repository import (
    get_references,
    create_reference,
    get_reference,
    delete_reference,
    edit_reference
    )
from entities.reference import Reference

@patch("repositories.reference_repository.db")
def test_get_references(mock_db):

    # mock database with two reference entries
    mock_result = MagicMock()
    mock_result.mappings().all.return_value = [
        {"id": 1, "cite_key": "key1", "title": "Title 1", "author": "Author 1", "year": 2020, "publisher": "Publisher A"},
        {"id": 2, "cite_key": "key2", "title": "Title 2", "author": "Author 1; Author 2", "year": 2021, "publisher": "Publisher B"},
    ]
    # mock result
    mock_db.session.execute.return_value = mock_result

    references = get_references()

    # test for correct amount of results
    assert len(references) == 2
    # test that the results are references
    assert all(isinstance(r, Reference) for r in references)
    # test a specific field
    assert references[0].title == "Title 1"
    # check that the function only made one query
    mock_db.session.execute.assert_called_once()


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

    create_reference(reference)

    # check that execute gets called
    mock_db.session.execute.assert_called_once()

    # check that the function uses correct parameters
    called_args, called_kwargs = mock_db.session.execute.call_args
    sql = str(called_args[0])
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert "INSERT INTO references_table" in sql
    assert params["reference_type"] == "book"
    assert params["cite_key"] == "key3"
    assert params["title"] == "Title 3"
    assert params["author"] == "Author 3"
    assert params["year"] == 2022
    assert params["publisher"] == "Publisher C"
    assert params["chapter"] == "Chapter 1"

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

    create_reference(reference)

    # check that execute gets called
    mock_db.session.execute.assert_called_once()

    # check that the function uses correct parameters
    called_args, called_kwargs = mock_db.session.execute.call_args
    sql = str(called_args[0])
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert "INSERT INTO references_table" in sql
    assert params["reference_type"] == "article"
    assert params["cite_key"] == "key4"
    assert params["title"] == "Article Title"
    assert params["author"] == "Article Author"
    assert params["year"] == 2023
    assert params["journal"] == "Journal X"
    assert params["volume"] == "42"
    assert params["pages"] == "10-20"

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

    create_reference(reference)

    # check that execute gets called
    mock_db.session.execute.assert_called_once()

    # check that the function uses correct parameters
    called_args, called_kwargs = mock_db.session.execute.call_args
    sql = str(called_args[0])
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert "INSERT INTO references_table" in sql
    assert params["reference_type"] == "inproceedings"
    assert params["cite_key"] == "key5"
    assert params["title"] == "Inproc Title"
    assert params["author"] == "Inproc Author"
    assert params["year"] == 2024
    assert params["booktitle"] == "Proceedings Y"

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

    create_reference(reference)

    # check that execute gets called
    mock_db.session.execute.assert_called_once()

    # check that the function uses correct parameters
    called_args, called_kwargs = mock_db.session.execute.call_args
    sql = str(called_args[0])
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert "INSERT INTO references_table" in sql
    assert params["reference_type"] == "misc"
    assert params["cite_key"] == "key6"
    assert params["title"] == "Scrum (project management)"
    assert params["author"] == "Wikipedia"
    assert params["year"] == 2025
    assert params["url"] == "https://en.wikipedia.org/wiki/Scrum_(project_management)"

    # check that the function commits
    mock_db.session.commit.assert_called_once()

@patch("repositories.reference_repository.db")
def test_get_reference_found(mock_db):

    mock_result = MagicMock()
    mock_result.mappings().first.return_value = {"id": 1, "cite_key": "key1", "title": "Title 1", "author": "Author 1", "year": 2020, "publisher": "Publisher A"}
    mock_db.session.execute.return_value = mock_result

    ref = get_reference(1)

    assert isinstance(ref, Reference)
    assert ref.title == "Title 1"
    # ensure execute was called and id param forwarded
    mock_db.session.execute.assert_called_once()
    called_args, called_kwargs = mock_db.session.execute.call_args
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert params["id"] == 1


@patch("repositories.reference_repository.db")
def test_get_reference_not_found(mock_db):

    mock_result = MagicMock()
    mock_result.mappings().first.return_value = None
    mock_db.session.execute.return_value = mock_result

    ref = get_reference(999)
    assert ref is None
    mock_db.session.execute.assert_called_once()


@patch("repositories.reference_repository.db")
def test_delete_reference(mock_db):
    # call delete and ensure execute and commit are called with expected id
    delete_reference(5)

    mock_db.session.execute.assert_called_once()
    called_args, called_kwargs = mock_db.session.execute.call_args
    params = called_args[1] if len(called_args) > 1 else called_kwargs
    assert params["id"] == 5
    mock_db.session.commit.assert_called_once()


@patch("repositories.reference_repository.db")
def test_edit_reference(mock_db):
    reference_dict_test = {
        "reference_type": "book",
        "cite_key": "edited_key",
        "title": "Edited Title",
        "author": "Edited Author",
        "year": 2030,
        "publisher": "Edited Publisher"
    }

    reference = Reference(reference_dict_test)

    edit_reference(3, reference)

    # ensure execute was called once
    mock_db.session.execute.assert_called_once()
    called_args, called_kwargs = mock_db.session.execute.call_args
    sql = str(called_args[0])
    params = called_args[1] if len(called_args) > 1 else called_kwargs

    # check SQL and parameters
    assert "UPDATE references_table" in sql
    assert params["id"] == 3
    assert params["cite_key"] == "edited_key"
    assert params["title"] == "Edited Title"
    assert params["author"] == "Edited Author"
    assert params["year"] == 2030
    assert params["publisher"] == "Edited Publisher"

    # ensure commit was called
    mock_db.session.commit.assert_called_once()
