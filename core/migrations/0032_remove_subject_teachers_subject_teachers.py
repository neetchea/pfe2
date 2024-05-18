# Generated by Django 5.0.4 on 2024-05-18 11:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_remove_grade_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='teachers',
        ),
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ForeignKey(limit_choices_to={'user_type': 'teacher'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to=settings.AUTH_USER_MODEL),
        ),
    ]
