# Generated by Django 4.0.1 on 2022-01-23 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardsection',
            name='project_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Площадной объект'), (2, 'Линейный объект')]),
        ),
    ]