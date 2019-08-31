from django.contrib.auth.models import User
from django import forms


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.webm', '.ogg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def validate_user_existance(username):
    user = User.objects.get(pk=username)

    if user is not None:
        raise forms.ValidationError(u'User with this username already exists.')


def validate_email_existance(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        pass
    else:
        raise forms.ValidationError(u'User with this email already exists.')
