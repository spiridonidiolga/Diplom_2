class ApiConfig:
    BASE_URL = "https://stellarburgers.education-services.ru/api"


class RegistrationData:
    DEFAULT = {
        "email": "",
        "password": "testpassword123",
        "name": "Test User"
    }


class InvalidRegistrationData:
    MISSING_FIELDS = {
        "email": "test@test.com",
        "password": "pass"
    }
    
    WEAK_PASSWORD = {
        "email": "test@test.com",
        "password": "weakpass",
        "name": "User"
    }


class LoginData:
    VALID = {
        "email": "existing_user@test.com",
        "password": "existing_password"
    }


class InvalidLoginData:
    WRONG_PASSWORD = {
        "email": "existing_user@test.com",
        "password": "wrongpass"
    }
    
    NON_EXISTING_USER = {
        "email": "nonexistent@test.com",
        "password": "existing_password"
    }
