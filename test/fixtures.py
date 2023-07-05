import random

import pytest
from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.api.utils import API_URL, users


@pytest.fixture()
def log_admin(scope="module"):
    """Login as admin and get a valid token"""
    client = TestClient(app)
    admin = list(filter(lambda test_list: test_list['is_admin'] is True, users))[0]
    response = client.post(f"{API_URL}/admin/login", json={
        "email": f"{admin['name']}@email.com",
        "password": f"{admin['password']}"
    })

    if response.status_code != 200:
        raise Exception("Can't get admin token")

    token = response.json()['access_token']
    yield client, token


# login as user
@pytest.fixture(scope="module")
def log_user():
    """Login as user and get a valid token"""
    client = TestClient(app)
    pick_user = users[random.randint(0, len(users) - 1)]
    response = client.post(f"{API_URL}/user/login", json={
        "email": f"{pick_user['name']}@email.com",
        "password": f"{pick_user['password']}"
    })
    if response.status_code != 200:
        raise Exception("Can't get user token")

    token = response.json()['access_token']
    yield client, token
