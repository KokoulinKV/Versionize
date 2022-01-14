from django.db import models
from user.models import User, Company


class Project(models.Model):
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now=True)
    exp_date = models.DateField()
    next_upload = models.DateField()
    admin = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)


class Document(models.Model):
    STATUS_CHOICES = (
        ('Первичные', 'Первичные замечания'),
        ('Повторные', 'Повторные замечания'),
        ('Загружено', 'Загружено'),
        ('Просрочено', 'Просрочено'),
        ('Положительное', 'Положительное'),
        ('Отрицательное', 'Отрицательное'),
    )
    name = models.CharField(max_length=128)
    doc_path = models.FileField(upload_to='main_docs')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    # TODO Предусмотреть автоматическое заполнение ячейки version.
    #  Если ранее был загружен документ в раздел с идентичным section_id,
    #  то берём номер версии предыдущего + 1, если нет - 1.
    version = models.IntegerField()
    variation = models.IntegerField()
    # TODO Предусмотреть автоматический расчёт md5
    md5 = models.CharField(max_length=32)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=128, blank=True)


class Adjustment(models.Model):
    CODE_CHOICES = (
        (1, 'Введение усовершенствований'),
        (2, 'Изменение стандартов и норм'),
        (3, 'Дополнительные требования заказчика'),
        (4, 'Устранение ошибок'),
        (5, 'Другие причины'),
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    pages = models.CharField(max_length=512)
    code = models.CharField(max_length=1, choices=CODE_CHOICES)
    note = models.CharField(max_length=128, blank=True)
    body = models.CharField(max_length=256)


class Remark(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    body = models.CharField(max_length=1024)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent')
    created_at = models.DateTimeField(auto_now=True)
    body = models.CharField(max_length=1024)
