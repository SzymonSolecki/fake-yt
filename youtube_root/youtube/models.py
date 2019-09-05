from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, validate_user_existance
from django.urls import reverse

import os
import uuid

# Create your models here.


# Method used to create unique filenames for uploaded videos.
def get_file_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), extension)
    return os.path.join('video', filename)


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Uploads video to path return from function. Function get_file_path
    # is used to prevent two the same filenames.
    file = models.FileField(upload_to=get_file_path, blank=False, null=True,
                            validators=[validate_file_extension]
                            )
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             related_name='videos',
                             )

    def get_absolute_url(self):
        return reverse('video', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='likes',
                              on_delete=models.CASCADE)

    # value will carry like status
    # 0 = dislike
    # 1 = like
    value = models.SmallIntegerField(default=0, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = ''
        if self.value == 0:
            status = 'disliked'
        else:
            status = 'liked'

        return 'User {} {} {} video'.format(self.user.username, status, self.video.title)


class Comment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(blank=False, null=False, auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='comments')

    def __str__(self):
        return self.text
