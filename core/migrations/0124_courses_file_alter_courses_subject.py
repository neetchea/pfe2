# Generated by Django 5.0.4 on 2024-05-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0123_courses_is_additional_courses_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='courses/'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
