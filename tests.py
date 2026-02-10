import pytest
import requests
from datetime import datetime
from config import BASE_URL

class TestStellarBurgersAPI:
    
    def test_create_user(self, base_url):
        # Создание уникального пользователя
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        new_user = {
            "email": unique_email,
            "password": "testpassword123",
            "name": "Test User"
        }
        response = requests.post(f"{base_url}/auth/register", json=new_user)
        assert response.status_code == 200
        assert response.json()["success"] == True

        # Попытка создать уже существующего пользователя
        response = requests.post(f"{base_url}/auth/register", json=new_user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

        # Создание пользователя с неполными данными
        incomplete_user = {
            "email": "test@test.com",
            "password": "pass"
        }
        response = requests.post(f"{base_url}/auth/register", json=incomplete_user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"

    def test_user_login(self, registered_user, base_url):
        # Успешный вход
        login_data = {
            "email": registered_user["user_data"]["email"],
            "password": registered_user["user_data"]["password"]
        }
        response = requests.post(
            f"{base_url}/auth/login", 
            json=login_data
        )
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

        # Неверный пароль
        invalid_password_data = {
            "email": login_data["email"],
            "password": "wrongpassword"
        }
        response = requests.post(
            f"{base_url}/auth/login", 
            json=invalid_password_data
        )
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"

    def test_create_order(self, registered_user, valid_ingredients, base_url):
        # Создание заказа с авторизацией и ингредиентами
        order_data = {
            "ingredients": valid_ingredients
        }
        response = requests.post(
            f"{base_url}/orders", 
            json=order_data, 
            headers=registered_user["headers"]
        )
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.json()["success"] == True
        assert "number" in response.json()["order"]

        # Создание заказа без авторизации
        response = requests.post(f"{base_url}/orders", json=order_data)
        assert response.status_code == 401

        # Создание заказа без ингредиентов
        empty_order_data = {
            "ingredients": []
        }
        response = requests.post(
            f"{base_url}/orders", 
            json=empty_order_data, 
            headers=registered_user["headers"]
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

        # Создание заказа с невалидным ингредиентом
        invalid_ingredients = ["invalid_id"]
        response = requests.post(
            f"{base_url}/orders", 
            json={"ingredients": invalid_ingredients}, 
            headers=registered_user["headers"]
        )
        assert response.status_code == 500

    