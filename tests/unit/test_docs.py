from app import create_app


def test_docs_ui_is_served():
    client = create_app().test_client()
    response = client.get("/docs/")
    assert response.status_code == 200


def test_openapi_spec_is_served():
    client = create_app().test_client()
    response = client.get("/openapi.yaml")
    assert response.status_code == 200
    assert b"openapi:" in response.data


def test_root_redirects_to_docs():
    client = create_app().test_client()
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/docs/")
