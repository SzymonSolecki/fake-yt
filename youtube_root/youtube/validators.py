from django.contrib.auth.models import User


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.webm', '.ogg']
    if not ext.lower() in valid_extensions:
        # raise ValidationError(u'Unsupported file extension.')
        raise ValidationError('Unsupported file extension.', code='error')


def validate_user_existance(username):
    from django.core.exceptions import IntegrityError
    user = User.objects.get(pk=username)

    if user is not None:
        raise IntegrityError(u'Giver user already exists')
