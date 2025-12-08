import os
import sys
import types

# Insert a minimal fake `config` module so importing the repository does not
# try to import Flask (which may not be available in the test environment).
fake_config = types.ModuleType("config")
fake_config.test_env = True
fake_config.db = None
sys.modules["config"] = fake_config

import repositories.reference_repository as repo


def test_normalize_doi_plain():
    assert repo._normalize_doi("10.1000/xyz") == "10.1000/xyz"


def test_normalize_doi_prefix():
    assert repo._normalize_doi("doi:10.1000/xyz") == "10.1000/xyz"


def test_normalize_doi_url():
    assert repo._normalize_doi("https://doi.org/10.1000/xyz") == "10.1000/xyz"


def test_load_fixture_exists():
    # This repository includes fixtures under src/tests/fixtures
    fixture = repo._load_fixture_for_doi("10.9999/testdoi")
    assert isinstance(fixture, dict)
    assert fixture.get("message", {}).get("DOI") == "10.9999/testdoi"


def test_load_fixture_not_exists():
    assert repo._load_fixture_for_doi("10.9999/doesnotexist") is None
