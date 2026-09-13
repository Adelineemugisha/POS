from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    user_data = {
        "full_name": "Test User",
        "username": "testuser_create",
        "password": "testpass123",
        "role": "cashier",
        "email": "test@example.com",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["full_name"] == user_data["full_name"]
    assert response.json()["username"] == user_data["username"]
    assert response.json()["role"] == user_data["role"]
    assert response.json()["email"] == user_data["email"]
    assert "password" not in response.json()
    return response.json()["user_id"]


def test_get_user():
    user_data = {
        "full_name": "Test User Get",
        "username": "testuser_get",
        "password": "testpass123",
        "role": "cashier",
        "email": "test_get@example.com",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["user_id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    assert response.json()["username"] == "testuser_get"


def test_update_user():
    user_data = {
        "full_name": "Test User Update",
        "username": "testuser_update",
        "password": "testpass123",
        "role": "cashier",
        "email": "test_update@example.com",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["user_id"]
    update_data = {"full_name": "Updated Name", "role": "manager"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == update_data["full_name"]
    assert response.json()["role"] == update_data["role"]


def test_login():
    user_data = {
        "full_name": "Test User Login",
        "username": "testuser_login",
        "password": "testpass123",
        "role": "cashier",
        "email": "test_login@example.com",
    }
    client.post("/users", json=user_data)
    response = client.post("/users/login", data={"username": "testuser_login", "password": "testpass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]


def test_delete_user():
    user_data = {
        "full_name": "Test User Delete",
        "username": "testuser_delete",
        "password": "testpass123",
        "role": "cashier",
        "email": "test_delete@example.com",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["user_id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404