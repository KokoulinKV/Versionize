from django.db import models
from django.utils import timezone
from user.models import User
from main.models import Document


# Create your models here.
class Notification(models.Model):
    # 1 - Уведомление, 2 - Сообщение, 3 - Встреча и тд
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
    
