# Generated by Django 4.0.1 on 2022-02-06 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.company', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='section',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert_id', to=settings.AUTH_USER_MODEL, verbose_name='Эксперт'),
        ),
        migrations.AddField(
            model_name='section',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project', verbose_name='Проект'),
        ),
        migrations.AddField(
            model_name='section',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответственный'),
        ),
        migrations.AddField(
            model_name='remarksdocs',
            name='to_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.document', verbose_name='Документ'),
        ),
        migrations.AddField(
            model_name='remarksdocs',
            name='to_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.project', verbose_name='Проект'),
        ),
        migrations.AddField(
            model_name='remarksdocs',
            name='to_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.section', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='remark',
            name='expert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Эксперт'),
        ),
        migrations.AddField(
            model_name='remark',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='project',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ГИП'),
        ),
        migrations.AddField(
            model_name='document',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='comment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_comments', to='main.document', verbose_name='Документ'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.document', verbose_name='Документ'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section', verbose_name='Раздел'),
        ),
    ]
