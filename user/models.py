from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)
    phone = models.CharField(verbose_name='phone', max_length=20, null=True)
    patronymic = models.CharField(verbose_name='patronymic', max_length=30, null=True)


class Company(models.Model):
    name = models.CharField(verbose_name='company', max_length=64)
    phone = models.CharField(verbose_name='phone', max_length=20, null=True)
    email = models.EmailField
    manager = models.ForeignKey(User, on_delete=models.CASCADE)


class UserCompanyInfo(models.Model):
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='department', max_length=128, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    expert = models.BooleanField(verbose_name='expert', default=False)
    chief_project_engineer = models.BooleanField(verbose_name='chief_project_engineer', default=False)
    assistant = models.BooleanField(verbose_name='assistant', default=False)

