import pytest
from src.app import create_app

@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

def test_hello_endpoint(client):
    """Test the root endpoint."""
    response = client.get('/')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['message'] == 'Hello, Docker!'
    assert data['status'] == 'success'

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['service'] == 'python-docker'

def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    data = response.get_json()
    
    assert response.status_code == 404
    assert data['error'] == 'Not Found'
    assert data['status'] == 404 