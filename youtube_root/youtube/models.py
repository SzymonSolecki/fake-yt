from django.db import models
from django.contrib.auth.models import User

import os
import uuid

# Create your models here.


def get_file_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), extension)
    return os.path.join('video', filename)


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             related_name='videos')
    like = models.IntegerField(default=0, blank=True, null=False)
    dislike = models.IntegerField(default=0, blank=True, null=False)


class Comment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='comments')
