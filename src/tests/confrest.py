import pytest
from app import app
from db_helper import setup_db


@pytest.fixture(scope="session", autouse=True)
def init_test_db():
    """
    Create schema before test session. Uses db_helper.setup_db() which
    executes src/schema.sql and ensures references_table exists.
    """
    with app.app_context():
        setup_db()
    yield
