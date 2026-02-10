BASE_URL = "https://stellarburgers.education-services.ru/api"

REGISTER_DATA_TEMPLATE = {
    "email": "",
    "password": "testpassword123",
    "name": "Test User"
}

INVALID_REGISTER_DATA = {
    "missing_fields": {
        "email": "test@test.com",
        "password": "pass"
    },
    "wrong_password": {
        "email": "test@test.com",
        "password": "weakpass",
        "name": "User"
    }
}

LOGIN_DATA = {
    "email": "existing_user@test.com",
    "password": "existing_password"
}

INVALID_LOGIN_DATA = {
    "wrong_password": {
        "email": "existing_user@test.com",
        "password": "wrongpass"
    },
    "wrong_email": {
        "email": "nonexistent@test.com",
        "password": "existing_password"
    }
}
