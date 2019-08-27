from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    password = forms.CharField(label='Password', max_length=40,
                               widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=40,
                               widget=forms.PasswordInput())


class AddVideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    file = forms.FileField()
