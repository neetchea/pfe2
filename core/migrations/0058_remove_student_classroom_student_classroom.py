# Generated by Django 5.0.4 on 2024-05-24 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ManyToManyField(null=True, related_name='student', to='core.classroom'),
        ),
    ]
