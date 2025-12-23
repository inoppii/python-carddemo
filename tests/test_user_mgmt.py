import pytest
from src.models.models import User
from src.auth.security import get_password_hash

def test_user_crud_flow(client, db_session):
    # 1. Create User
    new_user_data = {
        "usr_id": "TESTCRUD",
        "first_name": "Test",
        "last_name": "User",
        "password": "secretpassword",
        "usr_type": "R"
    }
    response = client.post("/users/", json=new_user_data)
    assert response.status_code == 201
    assert response.json()["usr_id"] == "TESTCRUD"

    # 2. List Users
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert any(u["usr_id"] == "TESTCRUD" for u in users)

    # 3. Get Single User
    response = client.get("/users/TESTCRUD")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"

    # 4. Update User
    update_data = {"first_name": "UpdatedName"}
    response = client.put("/users/TESTCRUD", json=update_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "UpdatedName"

    # 5. Delete User
    response = client.delete("/users/TESTCRUD")
    assert response.status_code == 204

    # 6. Verify Deletion
    response = client.get("/users/TESTCRUD")
    assert response.status_code == 404
