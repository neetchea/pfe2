# Generated by Django 5.0.4 on 2024-05-24 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='matricule',
        ),
    ]
