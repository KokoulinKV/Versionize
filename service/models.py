from django.db import models
from django.utils import timezone
from user.models import User


# Create your models here.
class Notification(models.Model):
    # 1 - Создание проекта, 2 - Создание раздела, 3 - Приглашение к проекту
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User,
                                related_name='notification_to',
                                on_delete=models.CASCADE,
                                null=True)
    from_user = models.ForeignKey(User,
                                  related_name='notification_from',
                                  on_delete=models.CASCADE,
                                  null=True)
    data = models.DateTimeField(default=timezone.now())
    user_has_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Создан',)


class Tasks(models.Model):
    # 1 - Создание проекта, 2 - Создание раздела, 3 - Приглашение к проекту
    task_importance = models.IntegerField()
    task_name = models.CharField(max_length=128,
                                 verbose_name='Наименование',
                                 )
    task_description = models.CharField(max_length=128,
                                        blank=True,
                                        verbose_name='Примечание',)
    task_creator = models.ForeignKey(User,
                                     related_name='task_creator',
                                     on_delete=models.SET_NULL,
                                     null=True)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Создан',)
