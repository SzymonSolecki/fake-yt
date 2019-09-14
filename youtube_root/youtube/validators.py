from django.contrib.auth.models import User
from django import forms
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.forms import ValidationError
import magic


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


@deconstructible
class FileValidator:

    error_messages = {
        'max_size': ("Ensure this file size is not greater than %(max_size)s."
                     " Your file size is %(size)s."),
        'min_size': ("Ensure this file size is not less than %(min_size)s. "
                     "Your file size is %(size)s."),
        'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        print("YEEEEEEEEEEEEEEEET")
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                  'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                print("yeeeeeeeeeeeeeeet")
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)
