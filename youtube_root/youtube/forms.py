from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Video, Comment
from .validators import validate_email_existance


class LoginForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        pass


class RegisterModelForm(UserCreationForm):
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
