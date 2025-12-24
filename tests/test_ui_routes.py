from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root_returns_login_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Sign In - CardDemo" in response.text

def test_dashboard_returns_html():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Dashboard - CardDemo" in response.text

def test_admin_returns_html():
    response = client.get("/admin")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Admin Dashboard - CardDemo" in response.text
