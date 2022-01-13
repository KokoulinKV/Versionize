from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import User, Company


class UserRegistrationFrom(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите никнейм'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите email'}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите фамилию'}))
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите Отчество'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите номер телефона'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-8', 'placeholder': 'Повторите пароль'}))
    company = forms.ModelChoiceField(queryset=Company.objects.values_list('name', flat=True),
                                     widget=forms.Select(attrs={'class': 'form-control py-8',
                                                                'placeholder': 'Введите название компании'}))
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название отдела'}))
    expert = forms.BooleanField(required=False)
    chief_project_engineer = forms.BooleanField(required=False)
    assistant = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'image', 'first_name', 'last_name', 'patronymic', 'phone', 'password1', 'password2',
            'department',
            'company', 'expert', 'chief_project_engineer', 'assistant')


class CompanyRegistrationFrom(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название компании'}))

    class Meta:
        model = Company
        fields = ('name',)
