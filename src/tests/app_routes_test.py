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
