import pytest
from rest_framework.test import APIClient
from account.models import User
from post.models import Post

@pytest.mark.django_db
def test_create_post(api_client, ):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser")

    api_client.force_authenticate(user=user)

    response = api_client.post("/post/create/", {"text": "Hello, world!"})
    
    assert response.status_code == 201
    assert response.data["text"] == "Hello, world!"

@pytest.mark.django_db
def test_get_posts(api_client):
    response = api_client.get("/post/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_rate_post(api_client):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser")

    api_client.force_authenticate(user=user)

    post = Post.objects.create(text="Пост с оценкой", user=user)

    response = api_client.post(f"/post/{post.id}/rate/", {
        "rating": 5
    })

    assert response.status_code == 201
    assert response.data["rating"] == '5'
