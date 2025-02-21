import pytest
from post.models import Post, Comment
from account.models import User

@pytest.mark.django_db
def test_add_comment(api_client):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser", is_active = True)

    response = api_client.post("/account/login/", {
        "email": 'test@example.com',
        "password": 'Test1234'
    })

    post = Post.objects.create(text="Тестовый пост", user=user)
    response = api_client.post(f"/post/{post.id}/comment/create/", {"comment": "Тестовый комментарий", 'user':user.username})

    assert response.status_code == 201
    assert response.data["comment"] == "Тестовый комментарий"

@pytest.mark.django_db
def test_get_post_comments(api_client):
    user = User.objects.create_user(email="test@example.com", password="Test1234", username="testuser")
    post = Post.objects.create(text="Пост с комментами", user=user)
    Comment.objects.create(post=post, user="User1", comment="Комментарий 1")
    Comment.objects.create(post=post, user="User2", comment="Комментарий 2")

    response = api_client.get(f"/post/{post.id}/comment/")
    assert response.status_code == 200
    assert len(response.data) > 0
