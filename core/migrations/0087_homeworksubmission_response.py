# Generated by Django 5.0.4 on 2024-05-25 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_alter_classroom_teachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworksubmission',
            name='response',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
