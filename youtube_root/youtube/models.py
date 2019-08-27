from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    path = models.CharField(max_length=60)
    date_added = models.DateTimeField(blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             related_name='videos')
    like = models.IntegerField()
    dislike = models.IntegerField()


class Comment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(blank=False, null=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='comments')
