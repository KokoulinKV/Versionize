from django.db import models
from user.models import User

# * @TheSleepyNomad
# ? Модель для уведомлений пользователей
class Notification(models.Model):
    """
    Так как уведомления для пользователей доступны на всех страницах проекта,
    то для отображения используется кастомный тег из main.templatestags.lk_tags.py - notifications
    notification_type - тип уведомления. В текущей версии не используется полностью
    """
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
    user_has_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Создан',)


# * @TheSleepyNomad
# ? Модель для todoList
class Tasks(models.Model):
    """
    Модель используется в IndexView для отображения/получение/хранения задач пользователей
    task_importance - Статус срочности задачи. Может хранить следующее значения:
        1 - Задача без срочности(обычная)
        2 - Несрочная задача
        3 - Может потерпеть, но желательно выполнить скорее
        4 - Срочная задача
    """
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
