from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, validate_user_existance
from django.urls import reverse

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
    file = models.FileField(upload_to=get_file_path, blank=True, null=True,
                            validators=[validate_file_extension]
                            )
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             related_name='videos',
                             validators=[validate_user_existance])
    like = models.IntegerField(default=0, blank=True, null=False)
    dislike = models.IntegerField(default=0, blank=True, null=False)

    def get_absolute_url(self):
        return reverse('video', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='comments')

    def __str__(self):
        return self.text
