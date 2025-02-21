from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.text} - {self.created_at}'
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)
    user = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.user} - {self.comment}'
    

class Rating(models.Model):
    class RatingChoice(models.IntegerChoices):
        TOO_BAD = 1
        BAD = 2
        NORMAL = 3
        GOOD = 4
        EXCELLENT = 5

    post = models.ForeignKey(Post, related_name='post_ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RatingChoice.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_product_rating')
        ]

    def __str__(self):
        return f'{self.user}, rating - {self.rating}, postId {self.post}'