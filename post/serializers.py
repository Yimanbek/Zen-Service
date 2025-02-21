from rest_framework import serializers
from .models import Post, Rating, Comment

class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'user', 'created_at', 'average_rating']
        extra_kwargs = {'user': {'read_only': True}} 
        
    def get_average_rating(self, obj):
        ratings = obj.post_ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'comment', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['post', 'user', 'rating']

    def validate_rating(self, value):
        if value not in range(1, 6):
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value
