from app.config import settings
from jose import jwt
import pytest





def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123456@gmail.com", "password": "password123"})

    new_user = res.json()
    assert new_user['email'] == "hello123456@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user,client):
    res = client.post(
        "/auth/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = res.json()
    payload = jwt.decode(login_res.get("access_token"),
                         settings.secret_key, algorithms=[settings.algorithm])
    assert login_res.get("token_type") == "bearer"
    assert res.status_code == 200
#
#
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/auth/login", data={"username": email, "password": password})

    assert res.status_code == status_code
#     # assert res.json().get('detail') == 'Invalid Credentials'