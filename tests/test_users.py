import pytest
from rest_framework.test import APIClient
from account.models import User


@pytest.mark.django_db
def test_get_user_list(api_client):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser")
    response = api_client.get("/account/")
    assert response.status_code == 200
    assert len(response.data) > 0

