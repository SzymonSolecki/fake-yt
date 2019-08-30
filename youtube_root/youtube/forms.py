from django import forms
from django.contrib.auth.models import User
from .models import Video, Comment


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    password = forms.CharField(label='Password', max_length=40,
                               widget=forms.PasswordInput())


class RegisterModelForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }


class AddVideoModelForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ['title', 'description', 'file']


class AddCommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea
        }
