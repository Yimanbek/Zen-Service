from django.shortcuts import render
from .serializers import LoginSerializer, RegistrationSerializer, GetUrlActivateSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login
from rest_framework.authtoken.models import Token
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json
import requests


User = get_user_model()
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')


class GetUrlActivate(generics.GenericAPIView):
    serializer_class = GetUrlActivateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.activation_code or user.is_active:
                return Response({"error": "Пользователь уже активирован или код отсутствует"}, status=400)

            bot_username = config('BOT_USERNAME')
            link = f"https://t.me/{bot_username}?start={user.activation_code}"

            response_data = {
                "message": "Привяжите Telegram для активации:",
                "telegram_link": link
            }
            return Response({"user": serializer.data, "telegram_info": response_data}, status=201)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                activation_code = user.activation_code
                bot_username = config('BOT_USERNAME')
                link = f"https://t.me/{bot_username}?start={activation_code}"
                response_data = {
                    "message": "Успешная регистрация! Привяжите Telegram для активации:",
                    "telegram_link": link
                }
                return Response({"user": serializer.data, "telegram_info": response_data}, status=201)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)

                if token:
                    data = {
                    'id':user.id,
                    'username': user.username,
                    'email': user.email,
                    }
                    return Response({'user':data,'token':token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        message = data.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        if text.startswith("/start"):
            parts = text.split()
            if len(parts) > 1:
                code = parts[1]

                try:
                    user = User.objects.get(activation_code=code)
                    user.telegram_chat_id = chat_id
                    user.is_active = True
                    user.activation_code = ''
                    user.save()

                    send_telegram_message(chat_id, "Аккаунт успешно привязан к Telegram!")
                except User.DoesNotExist:
                    send_telegram_message(chat_id, "Неверный код!")
            else:
                send_telegram_message(chat_id, "Привет! Укажи код после /start.")
        
        return JsonResponse({"ok": True})


def send_telegram_message(chat_id, text):
    TOKEN = config('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})
