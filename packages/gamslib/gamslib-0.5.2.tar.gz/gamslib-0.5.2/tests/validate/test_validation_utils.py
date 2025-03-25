import os

import pytest
import requests
import uritools

from gamslib.validate import utils


def test_load_scheme_from_file(shared_datadir):
    "Test loading a schema reference which ist not an uri."
    assert utils.load_schema(os.path.join(shared_datadir, "foo.txt")) == b"foo"

    # try to load a non-existing file
    with pytest.raises(ValueError, match="Cannot open schema file") as exp:
        utils.load_schema("missing.rng")


def test_load_schema_from_fileuri(shared_datadir, monkeypatch):
    # Load schema from file:// URI
    uri = uritools.uricompose(
        scheme="file", path=os.path.join(shared_datadir, "foo.txt")
    )
    assert utils.load_schema(uri) == b"foo"

    # Load non-existing schema from file:// URI
    uri = uritools.uricompose(
        scheme="file", path=os.path.join(shared_datadir, "missing.txt")
    )
    with pytest.raises(ValueError) as exp:
        utils.load_schema(uri)
    assert "Cannot open schema file" in str(exp.value)


def test_load_schema_from_url(monkeypatch):
    "Test loading a schema file from URL."

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"foo"

    # found the schema
    monkeypatch.setattr(utils.requests, "get", lambda url: mock_response)
    uri = "http://example.com/schema.rng"
    assert utils.load_schema(uri) == b"foo"

    # url leads to a 404
    mock_response._content = None
    mock_response.status_code = 404
    monkeypatch.setattr(utils.requests, "get", lambda url: mock_response)
    with pytest.raises(ValueError, match="Cannot open schema file"):
        utils.load_schema("http://example.com/missing.rng")


def test_load_schema_unknown_uri_scheme():
    "Test loading a schema file from uri with an unknown scheme should result in an error."

    with pytest.raises(ValueError, match="I do not know how to open"):
        utils.load_schema("ftp://example.com/schema.rng")
