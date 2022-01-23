from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    image = models.ImageField(
        upload_to='users_image',
        blank=True,
        verbose_name='Изображение',
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        null=True,
    )
    patronymic = models.CharField(verbose_name='Отчество',
                                  max_length=30,
                                  null=True)

    def get_fullname(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def get_usercompany_info(self):
        return UserCompanyInfo.objects.get(user_id=self.id)

    def get_company(self):
        user_company_info = self.get_usercompany_info()
        return user_company_info.company

    def get_position(self):
        user_company_info = self.get_usercompany_info()
        return user_company_info.position

    def get_project_role(self):
        user_company_info = self.get_usercompany_info()
        if user_company_info.expert:
            return 'Эксперт'
        elif user_company_info.chief_project_engineer:
            return 'ГИП'
        elif user_company_info.assistant:
            return 'Ассистент'
        else:
            return 'Пользователь'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"


class Company(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=64,
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Номер телефона',
    )
    email = models.EmailField(
        max_length=256,
        null=True,
        verbose_name='Эл. почта',
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Менеджер',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = "Компании"


class UserCompanyInfo(models.Model):
    user = models.OneToOneField(
        User,
        unique=True,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    department = models.CharField(
        verbose_name='Отделение',
        max_length=128,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Организация',
        blank=True,
        null=True
    )
    expert = models.BooleanField(
        default=False,
        verbose_name='Эксперт',
    )
    chief_project_engineer = models.BooleanField(
        default=False,
        verbose_name='ГИП',
    )
    assistant = models.BooleanField(
        default=False,
        verbose_name='Помощник',
    )
    position = models.CharField(
        verbose_name='Роль',
        max_length=128,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = "Организации"
