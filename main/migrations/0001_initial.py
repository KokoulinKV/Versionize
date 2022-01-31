# Generated by Django 4.0.1 on 2022-01-31 07:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adjustment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages', models.CharField(max_length=512, verbose_name='Лист')),
                ('code', models.CharField(choices=[('1', 'Введение усовершенствований'), ('2', 'Изменение стандартов и норм'), ('3', 'Дополнительные требования заказчика'), ('4', 'Устранение ошибок'), ('5', 'Другие причины')], max_length=1, verbose_name='Шифр')),
                ('note', models.CharField(blank=True, max_length=128, verbose_name='Примечания')),
                ('body', models.CharField(max_length=256, verbose_name='Содержание')),
            ],
            options={
                'verbose_name': 'Корректировки',
                'verbose_name_plural': 'Корректировки',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('body', models.CharField(max_length=1024, verbose_name='Содержание')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('doc_path', models.FileField(upload_to='main_docs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Путь')),
                ('version', models.IntegerField(verbose_name='Версия')),
                ('variation', models.IntegerField(verbose_name='Изменение')),
                ('md5', models.CharField(max_length=32)),
                ('status', models.CharField(blank=True, choices=[('Первичные', 'Первичные замечания'), ('Повторные', 'Повторные замечания'), ('Загружено', 'Загружено'), ('Просрочено', 'Просрочено'), ('Положительное', 'Положительное'), ('Отрицательное', 'Отрицательное')], max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Создан')),
                ('note', models.CharField(blank=True, max_length=128, verbose_name='Примечание')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, verbose_name='Шифр')),
                ('name', models.CharField(max_length=512, verbose_name='Наименование')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('exp_date', models.DateField(blank=True, null=True, verbose_name='Срок экспертизы')),
                ('next_upload', models.DateField(blank=True, null=True, verbose_name='Следующая загрузка')),
                ('project_type', models.IntegerField(blank=True, choices=[(2, 'Линейный'), (1, 'Площадной')], null=True, verbose_name='Тип объекта')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='№')),
                ('date', models.DateField(verbose_name='Дата')),
                ('body', models.CharField(max_length=1024, verbose_name='Содержание')),
                ('link', models.CharField(blank=True, max_length=256, verbose_name='Ссылка')),
                ('basis', models.CharField(blank=True, max_length=512, verbose_name='Основание')),
            ],
            options={
                'verbose_name': 'Замечание',
                'verbose_name_plural': 'Замечания',
            },
        ),
        migrations.CreateModel(
            name='RemarksDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('doc_path', models.FileField(upload_to='main_remarks', verbose_name='Путь')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Создан')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование')),
                ('abbreviation', models.CharField(max_length=16, verbose_name='Аббревиатура')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='StandardSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=256)),
                ('project_type', models.IntegerField(blank=True, choices=[(2, 'Линейный'), (1, 'Площадной')], null=True)),
            ],
        ),
    ]
