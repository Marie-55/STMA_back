import requests

BASE_URL = "http://127.0.0.1:5000/users"

def test_create_user():
    response = requests.post(f"{BASE_URL}/1", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    assert response.json()["message"] == "User created"

def test_get_user():
    response = requests.get(f"{BASE_URL}/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"

def test_update_user():
    response = requests.put(f"{BASE_URL}/1", json={"email": "alice.new@example.com"})
    assert response.status_code == 200
    assert response.json()["message"] == "User updated"

def test_delete_user():
    response = requests.delete(f"{BASE_URL}/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

if __name__ == "__main__":
    test_create_user()
    test_get_user()
    test_update_user()
    test_delete_user()
    print("All tests passed!")
