# Generated by Django 5.0.4 on 2024-05-28 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0126_alter_courses_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classroom', to='core.classroom'),
        ),
    ]
