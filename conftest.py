import pytest
from config import ApiConfig
from helpers import ApiHelper

@pytest.fixture(scope="session")
def base_url():
    return ApiConfig.BASE_URL

@pytest.fixture(scope="session")
def registered_user(base_url):
    user_data = ApiHelper.create_registered_user()
    
    yield user_data
    
    ApiHelper.delete_user(headers=user_data["headers"])

@pytest.fixture(autouse=True)
def cleanup_users():
    
    user_tokens = []
        
    def register_and_track(response):
        user_tokens.append(response.json()['accessToken'])
       
    original_register = ApiHelper.register_user
    
    def wrapped_register(*args, **kwargs):
        response = original_register(*args, **kwargs)
        register_and_track(response)
        return response
    
    ApiHelper.register_user = wrapped_register
    
    yield
       
    for token in user_tokens:
        try:
            ApiHelper.delete_user(
                headers={"Authorization": f"Bearer {token}"}
            )
        except Exception:
            pass