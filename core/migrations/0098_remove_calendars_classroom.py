# Generated by Django 5.0.4 on 2024-05-27 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_alter_grade_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendars',
            name='classroom',
        ),
    ]
