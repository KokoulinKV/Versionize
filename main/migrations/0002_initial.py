# Generated by Django 4.0.1 on 2022-01-17 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company'),
        ),
        migrations.AddField(
            model_name='section',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project'),
        ),
        migrations.AddField(
            model_name='section',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='remark',
            name='expert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='remark',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section'),
        ),
        migrations.AddField(
            model_name='project',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.document'),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main.comment'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.document'),
        ),
        migrations.AddField(
            model_name='adjustment',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.section'),
        ),
    ]
