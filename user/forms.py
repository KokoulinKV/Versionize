from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'auth-form__control', 'placeholder': 'Введите email'}
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'auth-form__control', 'placeholder': 'Введите пароль'}
        ))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('password', 'email', 'remember_me')
