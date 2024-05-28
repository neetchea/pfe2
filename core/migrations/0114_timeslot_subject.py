# Generated by Django 5.0.4 on 2024-05-28 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0113_alter_timeslot_time_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timeslots', to='core.subject'),
        ),
    ]
