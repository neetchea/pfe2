# Generated by Django 5.0.4 on 2024-05-31 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0129_alter_classroom_level_alter_courses_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
