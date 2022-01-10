from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)


class UserCompanyInfo(models.Model):
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='department', max_length=128, blank=True)
    company = models.CharField(verbose_name='company', max_length=128, blank=True)
    expert = models.BooleanField(verbose_name='expert', default=False)
    chief_project_engineer = models.BooleanField(verbose_name='chief_project_engineer', default=False)
    assistant = models.BooleanField(verbose_name='assistant', default=False)

