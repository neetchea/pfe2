# Generated by Django 5.0.4 on 2024-05-24 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_student_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='teacher',
        ),
    ]
