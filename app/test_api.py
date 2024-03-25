# test_api.py

import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from mongomock import MongoClient
from datetime import datetime, timedelta


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()




def test_register(test_client):
    response = test_client.post("/register", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_login(test_client):
    response = test_client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_blog(test_client):
    login_response = test_client.post("/login", json={"username": "test_user", "password": "test_password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/blogs", headers=headers, json={"title": "Test Blog", "content": "Test Content", "author": "test_user"})
    assert response.status_code == 200
    assert response.json()["message"] == "Blog created successfully"


def test_retrieve_blogs_authenticated(test_client):
    login_response = test_client.post("/login", json={"username": "test_user", "password": "test_password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/blogs", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_profile_authenticated(test_client):
    login_response = test_client.post("/login", json={"username": "test_user", "password": "test_password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.put("/profile", headers=headers, json={"name": "new_test_user"})
    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"



def test_retrieve_all_blogs(test_client):
    response = test_client.get("/blogs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_retrieve_blogs_by_tag(test_client):
    response = test_client.get("/blogs/tags/tag_name")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_delete_blog(test_client):
    login_response = test_client.post("/login", json={"username": "test_user", "password": "test_password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    test_client.post("/blogs", headers=headers, json={"title": "Test Blog 2", "content": "Test Content", "author": "test_user"})
    response = test_client.delete("/blogs", headers=headers, json={"title": "Test Blog 2"})
    assert response.status_code == 200
    assert response.json()["message"] == "Blog deleted successfully"


if __name__ == "__main__":
    pytest.main()
