from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User, Company, UserCompanyInfo


class UserRegistrationForm(UserCreationForm):
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

    class Meta:
        model = User
        fields = (
            'username', 'email', 'image', 'first_name', 'last_name', 'patronymic', 'phone', 'password1', 'password2',
        )


class UserAddInfoForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.select_related().exclude(id__in=(UserCompanyInfo.objects.values('user'))),
        empty_label='Выберете пользователя',
        widget=forms.Select(attrs={'class': 'form-control py-8',
                                   'placeholder': 'Выберите название организации'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label='Выберите организацию',
                                     widget=forms.Select(attrs={'class': 'form-control py-8',
                                                                'placeholder': 'Введите название организации'}))
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название отдела'}))
    expert = forms.BooleanField(required=False)
    chief_project_engineer = forms.BooleanField(required=False)
    assistant = forms.BooleanField(required=False)

    class Meta:
        model = UserCompanyInfo
        fields = ('__all__')


class UserCompanyInfoForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label=None,
                                     widget=forms.Select(attrs={'class': 'form-control py-8',
                                                                'placeholder': 'Введите название организации'}))
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название отдела'}))
    expert = forms.BooleanField(required=False)
    chief_project_engineer = forms.BooleanField(required=False)
    assistant = forms.BooleanField(required=False)

    class Meta:
        model = UserCompanyInfo
        fields = ('company', 'department', 'expert', 'chief_project_engineer', 'assistant',)


class CompanyRegistrationFrom(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название организации'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите номер телефона'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите email'}))

    class Meta:
        model = Company
        fields = ('name', 'phone', 'email',)


class CompanyEditForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите название организации'}))
    manager = forms.ModelChoiceField(queryset=User.objects.select_related().exclude(
        id__in=(Company.objects.filter(manager__isnull=False).values('manager'))), empty_label='Выберете пользователя',
        widget=forms.Select(attrs={'class': 'form-control py-8'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите номер телефона'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-8', 'placeholder': 'Введите email'}))

    class Meta:
        model = Company
        fields = ('name', 'manager', 'phone', 'email',)
