from unittest.mock import MagicMock, patch
from repositories.reference_repository import get_references, create_reference
from entities.reference import Reference

@patch("repositories.reference_repository.db")
def test_get_references(mock_db):

    # mock database with two reference entries
    mock_result = MagicMock()
    mock_result.mappings().all.return_value = [
        {"id": 1, "cite_key": "key1", "title": "Title 1", "year": 2020, "publisher": "Publisher A"},
        {"id": 2, "cite_key": "key2", "title": "Title 2", "year": 2021, "publisher": "Publisher B"},
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
def test_create_reference(mock_db):
    reference_dict_test = {
        "cite_key": "key3",
        "title": "Title 3",
        "year": 2022,
        "publisher": "Publisher C"
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
    assert params["cite_key"] == "key3"
    assert params["title"] == "Title 3"
    assert params["year"] == 2022
    assert params["publisher"] == "Publisher C"

    # check that the function commits
    mock_db.session.commit.assert_called_once()
