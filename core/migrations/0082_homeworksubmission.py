# Generated by Django 5.0.4 on 2024-05-25 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_homeworkassignment_assignment_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_file', models.FileField(blank=True, null=True, upload_to='homework_submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='core.homeworkassignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_submissions', to='core.student')),
            ],
        ),
    ]
