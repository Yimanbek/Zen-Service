from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer, RatingSerializer
from .models import Post, Comment, Rating
from rest_framework import generics, permissions, views
from account.permissions import IsAuthor
from rest_framework.response import Response
from rest_framework import status
from .telegram_bot import send_telegram_message



class PostListViews(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.prefetch_related('post_ratings')


class PostCreateViews(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user) 
        author = post.user

        if author.telegram_chat_id:
            send_telegram_message(author.telegram_chat_id, post)


class PostAdminAndAuthorDetailViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAuthor(), permissions.IsAdminUser()]

class CommentViews(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Пост не найден"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['post'] = post_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentListViews(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if not Post.objects.filter(id=post_id).exists():
            raise Response({"error": "Пост не найден"}, status=status.HTTP_404_NOT_FOUND)
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    
class CommentAdminViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
class RatingCreateUpdateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAdminUser(), IsAuthor()]
        return [permissions.IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Пост не найден"}, status=status.HTTP_404_NOT_FOUND)

        rating, created = Rating.objects.get_or_create(post=post, user=user, defaults={"rating": request.data.get("rating")})

        if not created:
            rating.rating = request.data.get("rating")
            rating.save()
            return Response({"message": "Оценка обновлена", "rating": rating.rating}, status=status.HTTP_200_OK)

        return Response({"message": "Оценка добавлена", "rating": rating.rating}, status=status.HTTP_201_CREATED)
    
