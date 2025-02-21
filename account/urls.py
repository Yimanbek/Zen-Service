from django.urls import path, include
from .views import RegistrationView,LoginView, UserListView, TelegramWebhookView, GetUrlActivate


urlpatterns = [
    path('account/register/', RegistrationView.as_view()),
    path('account/', UserListView.as_view()),
    path('account/login/',LoginView.as_view()),

    path('account/activate/get-url/',GetUrlActivate.as_view()),
    path('telegram/webhook/', TelegramWebhookView.as_view()),
]