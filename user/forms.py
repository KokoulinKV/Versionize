from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'auth-form__control',
                   'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'auth-form__control',
                                          'placeholder': 'Введите пароль'})
    )
    
    class Meta:
        model = User
        fields = ('password', 'email',)
