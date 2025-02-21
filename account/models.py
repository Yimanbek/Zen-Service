from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email should be provided')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser',False)
        return self._create_user(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('A staff user must have is_staff = True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('A superuser must have is_supersuer = True')
        return self._create_user(email, password, **kwargs)
    
class User(AbstractUser):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 100)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=255, blank=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code