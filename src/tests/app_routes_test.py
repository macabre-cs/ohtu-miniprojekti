from app import app
from unittest.mock import patch


@patch("app.create_reference")
def test_create_book_reference_success(mock_create):
    client = app.test_client()
    response = client.post(
        "/create_reference",
        data={
            "reference_type": "book",
            "cite_key": "key1",
            "title": "Title",
            "authors": ["Author One", "Author Two"],
            "year": "2020",
            "publisher": "Publisher",
        },
    )
    mock_create.assert_called_once()
    assert response.status_code == 302
    assert "/" in response.headers["Location"]


@patch("app.create_reference")
def test_create_article_reference_success(mock_create):
    client = app.test_client()
    response = client.post(
        "/create_reference",
        data={
            "reference_type": "article",
            "cite_key": "key1",
            "title": "Title",
            "authors": ["Author Three", "Author Four"],
            "year": "2021",
            "publisher": "Publisher",
            "journal": "Journal 1",
            "volume": "Volume 2",
            "pages": "10-20",
        },
    )
    mock_create.assert_called_once()
    assert response.status_code == 302
    assert "/" in response.headers["Location"]


@patch("app.create_reference")
def test_create_inproc_reference_success(mock_create):
    client = app.test_client()
    response = client.post(
        "/create_reference",
        data={
            "reference_type": "inproceedings",
            "cite_key": "key1",
            "title": "Title",
            "authors": ["Author Three", "Author Four"],
            "year": "2021",
            "booktitle": "TestBookTitle",
        },
    )
    mock_create.assert_called_once()
    assert response.status_code == 302
    assert "/" in response.headers["Location"]


@patch("app.create_reference")
def test_create_reference_missing_title(mock_create):
    client = app.test_client()
    response = client.post(
        "/create_reference",
        data={
            "reference_type": "book",
            "cite_key": "key1",
            "title": "",
            "authors": ["Author One"],
            "year": "2020",
            "publisher": "Publisher",
        },
        follow_redirects=True,
    )
    assert b"Title is required" in response.data
    mock_create.assert_not_called()


@patch("app.search_references_by_query")
def test_search_references_found(mock_search):
    mock_search.return_value = [
        {
            "id": 1,
            "reference_type": "book",
            "cite_key": "key2",
            "title": "New book",
            "author": "Author A",
            "year": 2021,
            "publisher": "Publisher B",
        }
    ]

    client = app.test_client()
    response = client.get("/search_references?query=new")

    assert response.status_code == 200
    assert b"New book" in response.data
    mock_search.assert_called_once_with("new")


@patch("app.search_references_by_query")
def test_search_references_no_query(mock_search):
    client = app.test_client()
    response = client.get("/search_references")

    assert response.status_code == 200
    assert b"Search results" not in response.data
    mock_search.assert_not_called()


@patch("app.search_references_by_query")
def test_search_references_not_found(mock_search):
    mock_search.return_value = []

    client = app.test_client()
    response = client.get("/search_references?query=NonExistent")

    assert response.status_code == 200
    assert b"Search results: 0" in response.data
    mock_search.assert_called_once_with("NonExistent")
