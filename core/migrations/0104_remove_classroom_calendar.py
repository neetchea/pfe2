# Generated by Django 5.0.4 on 2024-05-27 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0103_remove_calendars_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='calendar',
        ),
    ]
