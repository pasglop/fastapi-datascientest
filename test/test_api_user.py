import pytest
from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.api.v1.auth import signJWT
from app.utils import users

client = TestClient(app)

API_URL = "http://localhost:8081"


class TestAPIUser:

    def test_read_main(self):
        response = client.get(API_URL)
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test_user_connect_success(self):
        """Test the user connection to the API"""
        for user in users:
            response = client.post(f"{API_URL}/user/login", json={
                "email": f"{user['name']}@email.com",
                "password": user['password']
            })
            assert response.status_code == 200
            assert response.json()['access_token'] is not None

    def test_user_connect_fail(self):
        """Test the user connection to the API"""
        response = client.post(f"{API_URL}/user/login", json={
            "email": "unknow@email.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 200 \
               and response.json() == {"error": "Wrong login details!"}

    def test_admin_connect_success(self):
        """Test the admin connection to the API"""
        response = client.post(f"{API_URL}/admin/login", json={
            "email": "admin@email.com",
            "password": "4dm1N"
        })
        assert response.status_code == 200
        assert response.json()['access_token'] is not None

    def test_admin_connect_fail(self):
        """Test the admin connection to the API"""
        response = client.post(f"{API_URL}/admin/login", json={
            "email": "admin@email.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 200 \
               and response.json() == {"error": "Wrong login details!"}
