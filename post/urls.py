from django.urls import path
from .views import (
    PostListViews, 
    PostCreateViews, 
    PostAdminAndAuthorDetailViews, 
    CommentViews, 
    CommentListViews, 
    CommentAdminViews, 
    RatingCreateUpdateView
)

urlpatterns = [
    path("post/", PostListViews.as_view()),
    path("post/create/", PostCreateViews.as_view()),
    path("post/<int:pk>/", PostAdminAndAuthorDetailViews.as_view()),
    
    path("post/<int:post_id>/comment/", CommentListViews.as_view()),
    path("post/<int:post_id>/comment/create/", CommentViews.as_view()),
    path("comment/<int:pk>/", CommentAdminViews.as_view()),

    path("post/<int:post_id>/rate/", RatingCreateUpdateView.as_view()), 
]