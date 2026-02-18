import requests
from config import ApiConfig
from datetime import datetime

BASE_URL = ApiConfig.BASE_URL

class ApiHelper:
    @staticmethod
    def register_user(email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        return response

    @staticmethod
    def login_user(email, password):
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        return response

    @staticmethod
    def create_order(ingredients, headers=None):
        data = {
            "ingredients": ingredients
        }
        headers = headers or {}
        response = requests.post(f"{BASE_URL}/orders", json=data, headers=headers)
        return response

    @staticmethod
    def delete_user(headers):
        response = requests.delete(f"{BASE_URL}/auth/user", headers=headers)
        return response

    @staticmethod
    def create_registered_user():
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        register_data = {
            "email": unique_email,
            "password": "testpassword123",
            "name": "Test User"
        }
        
        response = ApiHelper.register_user(**register_data)
        assert response.status_code == 200
        data = response.json()
        
        return {
            "user_data": register_data,
            "auth_data": data,
            "headers": {
                "Authorization": f"Bearer {data['accessToken']}"
            }
        }
