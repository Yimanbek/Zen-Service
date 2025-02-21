from django.contrib import admin
from .models import Post, Comment, Rating

admin.site.register([Post, Comment, Rating])