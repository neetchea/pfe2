# Generated by Django 5.0.4 on 2024-05-27 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0104_remove_classroom_calendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendars',
            name='timeslots',
        ),
    ]
