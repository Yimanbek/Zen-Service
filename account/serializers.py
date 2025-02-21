from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=100, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password','telegram_chat_id','username')
    
    def validate(self, attrs):
        password = attrs['password']
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                {'password': {"letter_numbers": 'The password must contain letters and numbers'}}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("Пользователь неактивен.")
            else:
                raise serializers.ValidationError("Неправильные учетные данные.")
        else:
            raise serializers.ValidationError("Email и пароль обязательны.")

        return data
    

class GetUrlActivateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        if not user.check_password(password):
            raise serializers.ValidationError("Неправильный пароль.")

        data["user"] = user
        return data
