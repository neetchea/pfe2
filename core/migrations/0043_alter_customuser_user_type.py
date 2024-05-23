# Generated by Django 5.0.4 on 2024-05-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student'), ('parent', 'Parent'), ('admin/staff', 'Admin/Staff')], max_length=30),
        ),
    ]
