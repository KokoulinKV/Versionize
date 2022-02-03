import hashlib
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from user.models import User, Company
from service.models import Notification


class Project(models.Model):
    PROJECT_TYPE_CHOICES = {
        (1, 'Площадной'),
        (2, 'Линейный'),
    }
    code = models.CharField(
        max_length=64,
        verbose_name='Шифр',
    )
    name = models.CharField(
        max_length=512,
        verbose_name='Наименование',
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания',
    )
    exp_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Срок экспертизы',
    )
    next_upload = models.DateField(
        blank=True,
        null=True,
        verbose_name='Следующая загрузка',
    )
    admin = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='ГИП',
    )
    project_type = models.IntegerField(
        choices=PROJECT_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Тип объекта',
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.code

    def get_projects(self):
        return self.objects.all()

    def get_admin(self):
        return User.objects.get(id=self.admin.id)


@receiver(post_save, sender=Project)
def notification_for_users(sender, instance, created, **kwargs):
    """
    @TheSleepyNomad
    Функция будет создавать уведомления для пользователей, когда ГИП создает новый проект
    """
    # Выполянем кол, только если запись успешна создана
    if created:
        # Todo разобраться в ER-диаграмме БД и отправлять только тем пользователям, которых ГИП укажет в проекте
        # Делаем выборку всех пользователей, кроме ГИПа и для каждого из списка создаем уведомление
        users = User.objects.all().exclude(id=instance.admin.id)
        for user in users:
            notice = Notification.objects.create(
                notification_type=1,
                to_user=user,
                from_user=instance.admin)
            notice.save()


class StandardSection(models.Model):
    PROJECT_TYPE_CHOICES = {
        (1, 'Площадной'),
        (2, 'Линейный'),
    }
    abbreviation = models.CharField(
        max_length=16,
    )
    name = models.CharField(
        max_length=256,
    )
    project_type = models.IntegerField(
        choices=PROJECT_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.abbreviation


class Section(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Проект',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
    )
    # TODO поле не должно иметь возможности оставаться пустым при запуске проекта.
    #  Сделано для разработки.
    abbreviation = models.CharField(
        max_length=16,
        verbose_name='Аббревиатура',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Организация',
    )
    responsible = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        null=True,
        verbose_name='Ответственный',
    )
    expert = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='expert_id',
        verbose_name='Эксперт',
    )

    def __str__(self):
        return self.name

    def get_sections(self):
        return self.objects.all()

    def get_linked_documents(self):
        return Document.objects.filter(section=self).order_by('-created_at')

    def get_latest_linked_document(self):
        return Document.objects.filter(section=self).latest('created_at')

    def get_linked_remarks(self):
        return Remark.objects.filter(section=self).order_by('id')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    @receiver(post_save, sender=Project)
    def create_standard_sections(sender, instance, **kwargs):
        obj_sections = StandardSection.objects.filter(project_type=instance.project_type)
        for section in obj_sections:
            Section.objects.create(
                name=section.name,
                abbreviation=section.abbreviation,
                project=instance
            )


class Document(models.Model):
    STATUS_CHOICES = (
        ('Первичные', 'Первичные замечания'),
        ('Повторные', 'Повторные замечания'),
        ('Загружено', 'Загружено'),
        ('Просрочено', 'Просрочено'),
        ('Положительное', 'Положительное'),
        ('Отрицательное', 'Отрицательное'),
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование',
    )
    doc_path = models.FileField(
        upload_to='main_docs',
        verbose_name='Путь',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Раздел',
    )
    # TODO Предусмотреть автоматическое заполнение ячейки version.
    #  Если ранее был загружен документ в раздел с идентичным section_id,
    #  то берём номер версии предыдущего + 1, если нет - 1.
    version = models.IntegerField(
        verbose_name='Версия',
    )
    variation = models.IntegerField(
        verbose_name='Изменение',
    )
    # TODO Предусмотреть автоматический расчёт md5
    md5 = models.CharField(
        max_length=32,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Создан',
    )
    note = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Примечание',
    )

    def get_documents(self):
        return self.objects.all()

    # TODO предусмотреть функцию, которая будет сортировать на основании первой страницы изменений
    #  пример: номера страниц 3, 42, 44-48. С помощью regexp смотрим первую цифру и используем её для сортировки
    def get_linked_adjustments(self):
        return Adjustment.objects.filter(document=self).order_by('id')

    def get_doc_comments(self):
        return Comment.objects.filter(document=self).order_by('created_at')[::-1]

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new, not update old object in database!
            md5 = hashlib.md5()
            for chunk in self.doc_path.chunks():
                md5.update(chunk)
            self.md5 = md5.hexdigest()

        if Document.objects.filter(section_id=self.section):
            if not Document.objects.filter(md5=self.md5):
                last_vers_query = Document.objects.filter(
                    section_id=self.section).values('version')
                last_version = last_vers_query[len(last_vers_query) - 1]['version']
                self.version = last_version + 1
            else:
                raise ValidationError('')
        else:
            self.version = 1
        # TODO перенести на форму для вода значения пользователем, предварительно обдумав какие значения
        #  и как будут вводиться. Предлагаю для защиты оставить так.
        self.variation = self.version - 1
        return super(Document, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Adjustment(models.Model):
    CODE_CHOICES = (
        ('1', 'Введение усовершенствований'),
        ('2', 'Изменение стандартов и норм'),
        ('3', 'Дополнительные требования заказчика'),
        ('4', 'Устранение ошибок'),
        ('5', 'Другие причины'),
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Раздел',
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name='Документ',
    )
    pages = models.CharField(
        max_length=512,
        verbose_name='Лист',
    )
    code = models.CharField(
        max_length=1,
        choices=CODE_CHOICES,
        verbose_name='Шифр',
    )
    note = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Примечания',
    )
    body = models.CharField(
        max_length=256,
        verbose_name='Содержание',
    )

    class Meta:
        verbose_name = 'Корректировки'
        verbose_name_plural = 'Корректировки'

    def get_document_adjustments(self, selected_document_id):
        return self.objects.filter(document=selected_document_id)


class Remark(models.Model):
    number = models.IntegerField(
        verbose_name='№',
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Раздел',
    )
    expert = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Эксперт',
    )
    date = models.DateField(
        verbose_name='Дата',
    )
    body = models.CharField(
        max_length=1024,
        verbose_name='Содержание',
    )
    link = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Ссылка',
    )
    basis = models.CharField(
        max_length=512,
        blank=True,
        verbose_name='Основание',
    )

    def get_project_remarks(self):
        return self.objects.all()

    def get_section_remarks(self, selected_section_id):
        return self.objects.filter(section=selected_section_id)

    class Meta:
        verbose_name = 'Замечание'
        verbose_name_plural = 'Замечания'


class Comment(models.Model):
    """
    Данная таблица хранит в себе комментарии к документам.
    Для чата или уведомлений будет сделана новая модель, более подоходящая к этим сущностям
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    # recipient = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     related_name='recipient',
    #     verbose_name='Получатель',
    # )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        # blank=True,
        # null=True,
        verbose_name='Документ',
        related_name='doc_comments'
    )
    # reply_to = models.ForeignKey(
    #     'self',
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    #     related_name='parent',
    #     verbose_name='Переслать',
    # )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания',
    )
    body = models.CharField(
        max_length=1024,
        verbose_name='Содержание',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class RemarksDocs(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование',
    )
    doc_path = models.FileField(
        upload_to='main_remarks',
        verbose_name='Путь'
    )
    to_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Проект',
        blank=True,
        null=True,
    )
    to_section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Раздел',
        blank=True,
        null=True,
    )
    to_document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name='Документ',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Создан',
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name