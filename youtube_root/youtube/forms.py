from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Video, Comment
from .validators import validate_email_existance


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class RegisterModelForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address',
                             validators=[validate_email_existance])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddVideoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddVideoModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['file'].widget.attrs.update({'class': 'form-control-file'})

    class Meta:
        model = Video
        fields = ['title', 'description', 'file']


class AddCommentModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCommentModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea
        }
