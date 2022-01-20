from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)
    phone = models.CharField(verbose_name='phone', max_length=20, null=True)
    patronymic = models.CharField(verbose_name='patronymic', max_length=30, null=True)

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


class Company(models.Model):
    name = models.CharField(verbose_name='company', max_length=64)
    phone = models.CharField(verbose_name='phone', max_length=20, null=True)
    email = models.EmailField(max_length=256, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserCompanyInfo(models.Model):
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='department', max_length=128, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    expert = models.BooleanField(verbose_name='expert', default=False)
    chief_project_engineer = models.BooleanField(verbose_name='chief_project_engineer', default=False)
    assistant = models.BooleanField(verbose_name='assistant', default=False)
    position = models.CharField(verbose_name='position', max_length=128, blank=True)
