import pytest
from datetime import datetime
from helpers import ApiHelper
import allure

class TestStellarBurgersAPI:
    
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, base_url):
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        
        @allure.step("Регистрация пользователя с корректными данными")
        def register_user():
            return ApiHelper.register_user(
                email=unique_email,
                password="testpassword123",
                name="Test User"
            )
        
        response = register_user()
        assert response.status_code == 200
        assert response.json()["success"] == True
        
        @allure.step("Удаление созданного пользователя")
        def cleanup():
            ApiHelper.delete_user(
                headers={"Authorization": f"Bearer {response.json()['accessToken']}"}
            )
        
        cleanup()

    @allure.title("Попытка регистрации существующего пользователя")
    def test_register_existing_user(self, base_url):
        unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
        
        @allure.step("Первая регистрация пользователя")
        def first_registration():
            return ApiHelper.register_user(
                email=unique_email,
                password="testpassword123",
                name="Test User"
            )
            
        @allure.step("Вторая попытка регистрации того же пользователя")
        def second_registration():
            return ApiHelper.register_user(
                email=unique_email,
                password="testpassword123",
                name="Test User"
            )
            
        first_response = first_registration()
        response = second_registration()
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"
        
        @allure.step("Удаление пользователя после теста")
        def cleanup():
            ApiHelper.delete_user(
                headers={"Authorization": f"Bearer {first_response.json()['accessToken']}"}
            )
        
        cleanup()

    @allure.title("Регистрация пользователя с неполными данными")
    def test_register_without_required_fields(self, base_url):
        
        @allure.step("Попытка регистрации без поля name")
        def register_without_name():
            
            return ApiHelper.register_user(
                email="test@test.com",
                password="pass"
            )
            
        response = register_without_name()
        assert response.status_code == 400  
        assert response.json()["message"] == "Email, password and name are required fields"

    @allure.title("Успешная авторизация пользователя")
    def test_successful_login(self, registered_user):
        
        @allure.step("Авторизация с корректными данными")
        def login():
            return ApiHelper.login_user(
                email=registered_user["user_data"]["email"],
                password=registered_user["user_data"]["password"]
            )
            
        response = login()
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Авторизация с неверными данными")
    def test_login_with_wrong_credentials(self, registered_user):
        
        @allure.step("Попытка авторизации с неверным паролем")
        def wrong_login():
            return ApiHelper.login_user(
                email=registered_user["user_data"]["email"],
                password="wrongpassword123"
            )
            
        response = wrong_login()
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredients):
        
        @allure.step("Попытка создания заказа без токена")
        def create_order_without_token():
            return ApiHelper.create_order(ingredients=valid_ingredients)
            
        response = create_order_without_token()
        assert response.status_code == 401

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        
        @allure.step("Попытка создания заказа без ингредиентов")
        def create_empty_order():
            return ApiHelper.create_order(
                ingredients=[],
                headers=registered_user["headers"]
            )
            
        response = create_empty_order()
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, registered_user):
        
        @allure.step("Попытка создания заказа с некорректными ID ингредиентов")
        def create_invalid_order():
            invalid_ingredients = ["invalid_id"]
            return ApiHelper.create_order(
                ingredients=invalid_ingredients,
                headers=registered_user["headers"]
            )
            
        response = create_invalid_order()
        assert response.status_code == 500