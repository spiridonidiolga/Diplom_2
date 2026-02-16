import requests
from datetime import datetime
from config import ApiConfig
BASE_URL = ApiConfig.BASE_URL


class ApiHelper:
    BASE_URL = BASE_URL
    
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
