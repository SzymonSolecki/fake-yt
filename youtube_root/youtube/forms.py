from django import forms
from .validators import validate_file_extension
from django.contrib.auth.models import User
from .models import Video, Comment


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    password = forms.CharField(label='Password', max_length=40,
                               widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=40)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=40,
                               widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file']


class AddCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
