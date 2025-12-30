from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_view_card_list():
    response = client.get("/cards/list")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Credit Cards" in response.text

def test_view_account_view():
    response = client.get("/accounts/view")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Account View" in response.text

def test_view_transaction_reg():
    response = client.get("/transactions/reg")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Transaction Register" in response.text
