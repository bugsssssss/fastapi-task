# test_main.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base, engine

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

client = TestClient(app)

# ? Отключил, потому что у меня поле id должно быть unique
# def test_create_user():
#     response = client.post(
#         "/users/",
#         json={"full_name": "John Doe", "username": "john_doe",
#               "password": "securepassword"},
#     )
#     assert response.status_code == 200
#     assert response.json()["full_name"] == "John Doe"
#     assert response.json()["username"] == "john_doe"


def test_get_user_info():
    response = client.get("/users/3")
    assert response.status_code == 200
    assert response.json()["user_id"] == 3
    assert response.json()["username"] == "slu"


def test_update_user_info():
    response = client.put(
        "/users/4",
        json={
            "full_name": "Timur",
            "username": "tim",
            "password": "string"
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["full_name"] == "Timur"
    assert response.json()["username"] == "tim"

# ? Также отключил, каждый раз айди нужно вручную вбивать
# def test_delete_user():
#     response = client.delete("/users/3")
#     assert response.status_code == 200
#     assert response.json() == {"message": "User deleted successfully"}


def test_get_user_by_username():
    response = client.get("/users/?username=slu")
    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json()["full_name"] == "Ruslan"
    assert response.json()["username"] == "slu"


def test_login_for_access_token():
    response = client.post(
        "/token",
        json={"username": "andre",
              "password": "9008540"},
    )
    assert response.status_code == 200
    assert response.json()['access_token']


def test_read_users_me():
    # ? Нужно поменять на валидный
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmRyZSIsImV4cCI6MTcwMDA0MjU4OX0.LDJjBB7GzVWKxLe9nzGdDPJt_2vGPAvio-UGW6ZXigQ'
    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.json()['username'] == 'andre'
