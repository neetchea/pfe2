# Generated by Django 5.0.4 on 2024-05-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('teacher', 'Teacher'), ('student', 'Student'), ('parent', 'Parent')], max_length=10),
        ),
    ]
