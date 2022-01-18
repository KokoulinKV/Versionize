from django.db import models
from user.models import User, Company


class Project(models.Model):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now=True)
    exp_date = models.DateField()
    next_upload = models.DateField()
    admin = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)

    def get_projects(self):
        return self.objects.all()

    def get_admin(self):
        return User.objects.get(id=self.admin.id)


class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    responsible = models.ForeignKey(User,
                                    db_index=True,
                                    on_delete=models.CASCADE)
    expert = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='expert_id')

    def get_sections(self):
        return self.objects.all()

    def get_linked_documents(self):
        return Document.objects.filter(section=self).order_by('-created_at')

    def get_latest_linked_document(self):
        return Document.objects.filter(section=self).latest('created_at')

    def get_linked_remarks(self):
        return Remark.objects.filter(section=self).order_by('id')


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

    def get_documents(self):
        return self.objects.all()

    # TODO предусмотреть функцию, которая будет сортировать на основании первой страницы изменений
    #  пример: номера страниц 3, 42, 44-48. С помощью regexp смотрим первую цифру и используем её для сортировки
    def get_linked_adjustments(self):
        return Adjustment.objects.filter(document=self).order_by('id')


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

    def get_document_adjustments(self, selected_document_id):
        return self.objects.filter(document=selected_document_id)


class Remark(models.Model):
    number = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    body = models.CharField(max_length=1024)
    link = models.CharField(max_length=256, blank=True)
    basis = models.CharField(max_length=512, blank=True)

    def get_project_remarks(self):
        return self.objects.all()

    def get_section_remarks(self, selected_section_id):
        return self.objects.filter(section=selected_section_id)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='recipient')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 related_name='parent')
    created_at = models.DateTimeField(auto_now=True)
    body = models.CharField(max_length=1024)
