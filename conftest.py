import pytest
import requests
from datetime import datetime
from config import BASE_URL

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def registered_user(base_url):
    unique_email = f"test_user_{datetime.now().timestamp()}@test.com"
    register_data = {
        "email": unique_email,
        "password": "testpassword123",
        "name": "Test User"
    }
    
    response = requests.post(f"{base_url}/auth/register", json=register_data)
    assert response.status_code == 200
    data = response.json()
    
    yield {
        "user_data": register_data,
        "auth_data": data,
        "headers": {
            "Authorization": f"Bearer {data['accessToken']}"
        }
    }
    
    
    requests.delete(
        f"{base_url}/auth/user",
        headers={"Authorization": f"Bearer {data['accessToken']}"}
    )

@pytest.fixture
def unauthorized_headers():
    return {}

@pytest.fixture
def valid_ingredients():
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
