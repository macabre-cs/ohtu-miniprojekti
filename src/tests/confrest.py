import os
import pytest

from app import app
from db_helper import setup_db
from config import db

os.environ.setdefault("TEST_ENV", "true")


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """
    Prepare the database for tests by creating schema from schema.sql
    using db_helper.setup_db(). This runs once per test session.

    Teardown drops the references_table to avoid leftover state.
    """
    with app.app_context():
        setup_db()

    yield

    with app.app_context():
        db.session.execute("DROP TABLE IF EXISTS references_table")
        db.session.commit()
