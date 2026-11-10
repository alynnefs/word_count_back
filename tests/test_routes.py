import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_post_valid(client):
    res = client.post("/count", json={"text": "hello world"})
    assert res.status_code == 200
    assert res.get_json() == {"count": 2}


def test_post_empty_text(client):
    res = client.post("/count", json={"text": ""})
    assert res.status_code == 200
    assert res.get_json() == {"count": 0}


def test_post_missing_body(client):
    res = client.post("/count")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_post_text_not_string(client):
    res = client.post("/count", json={"text": 123})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_post_missing_text_field(client):
    res = client.post("/count", json={"other": "value"})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_post_text_too_long(client):
    res = client.post("/count", json={"text": "a" * 100001})
    assert res.status_code == 413
    assert "error" in res.get_json()


def test_get_legacy(client):
    res = client.get("/count/hello")
    assert res.status_code == 200
    assert res.data == b"1"


def test_get_legacy_empty(client):
    res = client.get("/count/")
    assert res.status_code == 200
    assert res.data == b"0"
