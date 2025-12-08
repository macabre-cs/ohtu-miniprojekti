import os
import json

import repositories.reference_repository as repo


def test_get_reference_by_doi_fixture_loading(tmp_path, monkeypatch):
    # ensure test-mode path is used
    monkeypatch.setattr(repo, "test_env", True)

    # canonical fixture for testdoi should exist in tests/fixtures
    res = repo.get_reference_by_doi("10.9999/testdoi")
    assert isinstance(res, dict)
    assert res.get("message", {}).get("DOI") == "10.9999/testdoi"

    # input variants: prefixed, full URL, padded whitespace
    res2 = repo.get_reference_by_doi("doi:10.9999/testdoi")
    assert res2.get("message", {}).get("DOI") == "10.9999/testdoi"

    res3 = repo.get_reference_by_doi("https://doi.org/10.9999/testdoi")
    assert res3.get("message", {}).get("DOI") == "10.9999/testdoi"

    res4 = repo.get_reference_by_doi(" 10.9999/testdoi ")
    assert res4.get("message", {}).get("DOI") == "10.9999/testdoi"


def test_get_reference_by_doi_missing_fixture_returns_none(monkeypatch):
    monkeypatch.setattr(repo, "test_env", True)
    res = repo.get_reference_by_doi("10.9999/doesnotexist")
    assert res is None
