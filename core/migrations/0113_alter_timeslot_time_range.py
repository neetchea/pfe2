# Generated by Django 5.0.4 on 2024-05-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0112_calendars_calendar_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='time_range',
            field=models.CharField(blank=True, choices=[('7:00 - 8:00', '7:00 - 8:00'), ('8:00 - 9:00', '8:00 - 9:00'), ('9:00 - 10:00', '9:00 - 10:00'), ('10:00 - 11:00', '10:00 - 11:00'), ('11:00 - 12:00', '11:00 - 12:00'), ('12:00 - 1:00', '12:00 - 1:00'), ('1:00 - 2:00', '1:00 - 2:00'), ('2:00 - 3:00', '2:00 - 3:00'), ('3:00 - 4:00', '3:00 - 4:00'), ('4:00 - 5:00', '4:00 - 5:00'), ('5:00 - 6:00', '5:00 - 6:00')], default='8:00 - 9:00', max_length=13, null=True),
        ),
    ]
