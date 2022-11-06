from datetime import datetime
from email.policy import default
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post_text = models.CharField(max_length = 10000)
    posting_time = models.DateTimeField(default = datetime.now)
    like_count = models.IntegerField(default =0)

    def __str__(self) -> str:
        return {self.post_text}
        

class likes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return {self.user.username, self.post.post_text}
        

class Follow(models.Model):
    followed_person = models.ForeignKey(User, on_delete = models.CASCADE, related_name="follow")
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name="following")

    def __str__(self) -> str:
        return {self.followed_person.username}
