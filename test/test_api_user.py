from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.api.utils import users, API_URL
from fixtures import log_user, log_admin

client = TestClient(app)

class TestAPIUser:

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
