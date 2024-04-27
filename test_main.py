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

def test_api_root(client: TestClient):
    r = client.get('/api/')
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    answer_type = data[0]['type']
    assert answer_type == 'Page'
    components = data[0]['components']
    assert len(components) == 4
    assert components[0]['type'] == 'Heading'
    assert components[1]['type'] == 'Image'
    assert components[2]['type'] == 'Div'
    assert components[3]['type'] == 'Table'
    