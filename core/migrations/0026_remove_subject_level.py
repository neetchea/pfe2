# Generated by Django 5.0.4 on 2024-05-18 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_subject_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='level',
        ),
    ]
