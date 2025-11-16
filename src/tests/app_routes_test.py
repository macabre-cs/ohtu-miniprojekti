from app import app
from unittest.mock import patch

@patch("app.create_reference")
def test_create_reference_success(mock_create):
    client = app.test_client()
    response = client.post("/create_reference", data={
        "cite_key": "key1",
        "title": "Title",
        "year": "2020",
        "publisher": "Publisher"
    })
    mock_create.assert_called_once()
    assert response.status_code == 302
    assert "/" in response.headers["Location"]

@patch("app.create_reference")
def test_create_reference_missing_title(mock_create):
    client = app.test_client()
    response = client.post("/create_reference", data={
        "cite_key": "key1",
        "title": "",
        "year": "2020",
        "publisher": "Publisher"
    }, follow_redirects=True)
    assert b"Title is required" in response.data
