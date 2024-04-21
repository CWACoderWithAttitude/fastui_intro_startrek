import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

#
# It's odd the next two test yield the same behaviour by calling different endpoints
#   -> i need to do this more often to understand
#
def test_get_index(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200, response.text
    assert response.text.startswith('<!doctype html>\n')
    
def test_get_index(client: TestClient):
    response = client.get('/api')
    assert response.status_code == 200, response.text
    assert response.text.startswith('<!doctype html>\n')

def test_add_new_ship(client: TestClient):
    ship_json = {
        "name": "USS Pytest",
        "sign": "NX-0815",
        "classification": "Test Framework",
        "speed": "42",
        "captain": "VSC",
        "comment": "to boldly go where no man has gone before"
    }
    response = client.post(
        "/api/ships/add?ships=USS-Pytest",
        json=ship_json,
    )
    assert response.status_code == 200

