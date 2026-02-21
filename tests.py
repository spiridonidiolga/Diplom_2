import pytest
from datetime import datetime
from config import ApiConfig, RegistrationData, InvalidRegistrationData
from helpers import ApiHelper
import allure

class TestUserRegistration:
    
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self):
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        registration_data = {
            **RegistrationData.DEFAULT,
            "email": unique_email
        }
        
        response = ApiHelper.register_user(**registration_data)
        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Проверка удаления зарегистрированного пользователя")
    def test_delete_registered_user(self):
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        registration_data = {
            **RegistrationData.DEFAULT,
            "email": unique_email
        }
                
        register_response = ApiHelper.register_user(**registration_data)
        headers = {"Authorization": f"Bearer {register_response.json()['accessToken']}"}
                
        delete_response = ApiHelper.delete_user(headers=headers)
        assert delete_response.status_code == 403 

    @allure.title("Проверка попытки повторной регистрации существующего пользователя")
    def test_register_existing_user(self):
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        registration_data = {
            **RegistrationData.DEFAULT,
            "email": unique_email
        }
    
        ApiHelper.register_user(**registration_data)
        
        response = ApiHelper.register_user(**registration_data)
        assert response.status_code == 403, "Должен быть запрещён повторный вход"
        assert response.json()["message"] == "User already exists", "Сообщение об ошибке должно быть корректным"

    @allure.title("Проверка регистрации с неполными данными")
    def test_register_without_required_fields(self):
        response = ApiHelper.register_user(**InvalidRegistrationData.MISSING_FIELDS)
        assert response.status_code == 400
        assert response.json()["message"] == "Email, password and name are required fields"

    @allure.title("Проверка успешной авторизации")
    def test_successful_login(self, registered_user):
        response = ApiHelper.login_user(
            email=registered_user["user_data"]["email"],
            password=registered_user["user_data"]["password"]
        )
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Проверка авторизации с неверным паролем")
    def test_login_with_wrong_credentials(self, registered_user):
        response = ApiHelper.login_user(
            email=registered_user["user_data"]["email"],
            password="wrongpassword123"
        )
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"

class TestOrderCreation:
    
    @allure.title("Проверка создания заказа без авторизации")
    def test_create_order_without_auth(self):
        response = ApiHelper.create_order(ingredients=ApiConfig.VALID_INGREDIENTS)
        assert response.status_code == 400

    @allure.title("Проверка создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        response = ApiHelper.create_order(
            ingredients=[],
            headers=registered_user["headers"]
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, registered_user):
        invalid_ingredients = ["invalid_id"]
        response = ApiHelper.create_order(
            ingredients=invalid_ingredients,
            headers=registered_user["headers"]
        )
        assert response.status_code == 500
