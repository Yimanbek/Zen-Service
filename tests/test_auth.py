import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register(api_client):
    response = api_client.post(
        "/account/register/", 
        {
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "username": "newuser"
        }
    )
    assert response.status_code == 201

@pytest.mark.django_db
def test_login(api_client):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser", is_active = True)

    response = api_client.post("/account/login/", {
        "email": "test@example.com",
        "password": 'Test1234'
    })
    assert response.status_code == 200
    assert "token" in response.data
